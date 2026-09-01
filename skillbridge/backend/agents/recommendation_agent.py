import json
from typing import TypedDict
from sqlalchemy.orm import Session

from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from utils.llm_setup import get_llm
from models.student import StudentProfile, StudentSkill, StudentProject
from models.opportunity import Opportunity
from models.course import Course
from models.assessment import StudentAssessment
from models.user import User


class RecommendationState(TypedDict):
    user_id: int
    profile_data: dict
    skill_data: list
    assessment_data: list
    opportunities: list
    matched_internships: list
    gap_courses: list
    career_advice: str
    has_assessments: bool
    message: str


@tool
def fetch_student_profile(user_id: int, db: Session) -> str:
    """Retrieves the complete student profile, skills, and assessment history."""
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        profile = StudentProfile(user_id=user_id, college="University", department="CS")
        db.add(profile)
        db.commit()
        db.refresh(profile)

    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all()
    assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == user_id).all()
    projects = db.query(StudentProject).filter(StudentProject.profile_id == profile.id).all()

    return json.dumps({
        "name": user.name if user else "Student",
        "department": profile.department,
        "cgpa": profile.cgpa,
        "skills": [{"name": s.skill_name, "self": s.self_rating, "verified": s.verified_rating, "is_verified": bool(s.is_verified)} for s in skills],
        "assessments": [{"skill": a.skill_name, "score": a.score, "level": a.verified_level} for a in assessments],
        "projects": [p.title for p in projects],
        "has_assessments": len(assessments) > 0,
    })


@tool
def fetch_and_rank_opportunities(profile_json: str, db: Session) -> str:
    """Fetches all active opportunities and computes weighted match scores against verified skills."""
    profile = json.loads(profile_json)
    if not profile.get("has_assessments"):
        return json.dumps({"matched": [], "reason": "No assessments"})

    skill_lookup = {}
    for s in profile["skills"]:
        eff = s["verified"] if s["is_verified"] and s["verified"] > 0 else s["self"] * 0.6
        skill_lookup[s["name"].lower().strip()] = {"eff": eff, "verified": s["is_verified"]}

    opps = db.query(Opportunity).filter(Opportunity.status == "active").all()
    matched = []

    for opp in opps:
        req_list = [r.strip().lower() for r in (opp.required_skills or "").split(",") if r.strip()]
        if not req_list:
            continue

        weight = 0.0
        missing = []
        ver_count = 0
        for req in req_list:
            if req in skill_lookup:
                info = skill_lookup[req]
                if info["verified"]:
                    ver_count += 1
                    weight += min((info["eff"] / 10.0) * 1.25, 1.0)
                else:
                    weight += (info["eff"] / 10.0) * 0.75
            else:
                missing.append(req.title())

        score = (weight / len(req_list)) * 100.0
        if profile.get("cgpa") and opp.min_cgpa and profile["cgpa"] >= opp.min_cgpa:
            score += 5.0
        score += min(len(profile["assessments"]) * 2.0, 10.0)
        score = round(min(max(score, 15.0), 100.0), 1)

        matched.append({
            "id": opp.id, "title": opp.title, "company_name": opp.company_name,
            "location": opp.location, "opportunity_type": opp.opportunity_type,
            "stipend": opp.stipend, "duration": opp.duration,
            "required_skills": opp.required_skills, "min_cgpa": opp.min_cgpa,
            "description": opp.description,
            "match_percentage": score, "match_score": score,
            "missing_skills": missing, "verified_skills_matched": ver_count,
        })

    matched.sort(key=lambda x: x["match_percentage"], reverse=True)
    return json.dumps({"matched": matched[:12]})


@tool
def identify_gaps_and_courses(profile_json: str, matched_json: str, db: Session) -> str:
    """Identifies weak skills from assessment scores and maps them to YouTube bridge courses."""
    profile = json.loads(profile_json)
    matched_data = json.loads(matched_json)

    weak_skills = set()
    for m in matched_data.get("matched", [])[:6]:
        for ms in m.get("missing_skills", []):
            weak_skills.add(ms.strip())
    for s in profile.get("skills", []):
        eff = s["verified"] if s["is_verified"] else s["self"] * 0.6
        if eff < 6.0:
            weak_skills.add(s["name"].strip())
    for a in profile.get("assessments", []):
        if a["score"] < 60:
            weak_skills.add(a["skill"].strip())

    gap_courses = []
    for skill in list(weak_skills)[:8]:
        courses = db.query(Course).filter(Course.skill_tags.ilike(f"%{skill}%")).all()
        if courses:
            curated = [{"title": c.title, "provider": c.provider, "youtube_url": c.url, "duration": f"{int(c.duration_hours)}h", "rating": c.rating, "is_free": bool(c.is_free)} for c in courses[:3]]
        else:
            curated = [{"title": f"Learn {skill.title()}", "provider": "YouTube", "youtube_url": f"https://www.youtube.com/results?search_query={skill.replace(chr(32), chr(43))}+full+course", "duration": "4-8h", "rating": 4.7, "is_free": True}]
        gap_courses.append({"skill": skill.title(), "weak_skill": skill.title(), "courses": curated})

    return json.dumps({"gap_courses": gap_courses})


@tool
def generate_ai_career_advice(profile_json: str, matched_json: str) -> str:
    """Calls Groq Llama-3.3-70B to generate personalized career strategy advice."""
    profile = json.loads(profile_json)
    matched_data = json.loads(matched_json)

    if not profile.get("has_assessments"):
        return ""

    llm = get_llm()
    skill_text = ", ".join([f"{s[chr(110)+chr(97)+chr(109)+chr(101)]} ({s[chr(118)+chr(101)+chr(114)+chr(105)+chr(102)+chr(105)+chr(101)+chr(100)]}/10)" if s["is_verified"] else f"{s[chr(110)+chr(97)+chr(109)+chr(101)]} (Self: {s[chr(115)+chr(101)+chr(108)+chr(102)]}/10)" for s in profile.get("skills", [])])
    top_matches = ", ".join([m["title"] for m in matched_data.get("matched", [])[:3]])

    prompt = f"Career coaching for Indian student: {profile[chr(110)+chr(97)+chr(109)+chr(101)]}, Dept: {profile[chr(100)+chr(101)+chr(112)+chr(97)+chr(114)+chr(116)+chr(109)+chr(101)+chr(110)+chr(116)]}, CGPA: {profile[chr(99)+chr(103)+chr(112)+chr(97)]}, Skills: {skill_text}, Top Matches: {top_matches}. Give 3 actionable bullet points including AYUSH sector."

    response = llm.invoke(prompt)
    return response.content


# ── LangGraph Nodes ──
def node_fetch_profile(state: RecommendationState, db: Session) -> dict:
    """Node 1: Fetch student profile (LangSmith trace)"""
    raw = fetch_student_profile.invoke({"user_id": state["user_id"], "db": db})
    data = json.loads(raw)
    return {"profile_data": data, "has_assessments": data.get("has_assessments", False)}

def node_rank_opportunities(state: RecommendationState, db: Session) -> dict:
    """Node 2: Rank opportunities (LangSmith trace)"""
    if not state.get("has_assessments"):
        return {"matched_internships": [], "message": "Complete at least one assessment to unlock recommendations."}
    raw = fetch_and_rank_opportunities.invoke({"profile_json": json.dumps(state["profile_data"]), "db": db})
    data = json.loads(raw)
    return {"matched_internships": data.get("matched", [])}

def node_find_gaps(state: RecommendationState, db: Session) -> dict:
    """Node 3: Identify gaps and courses (LangSmith trace)"""
    if not state.get("has_assessments"):
        return {"gap_courses": []}
    raw = identify_gaps_and_courses.invoke({
        "profile_json": json.dumps(state["profile_data"]),
        "matched_json": json.dumps({"matched": state.get("matched_internships", [])}),
        "db": db
    })
    data = json.loads(raw)
    return {"gap_courses": data.get("gap_courses", [])}

def node_career_advice(state: RecommendationState, db: Session) -> dict:
    """Node 4: Generate AI career advice (LangSmith trace)"""
    if not state.get("has_assessments"):
        return {"career_advice": ""}
    advice = generate_ai_career_advice.invoke({
        "profile_json": json.dumps(state["profile_data"]),
        "matched_json": json.dumps({"matched": state.get("matched_internships", [])})
    })
    return {"career_advice": advice}


# ── Public API ──
def get_recommendations(user_id: int, db: Session) -> dict:
    """Runs the full 4-node recommendation pipeline (all steps in LangSmith)."""

    graph = StateGraph(RecommendationState)
    graph.add_node("fetch_profile", lambda s: node_fetch_profile(s, db))
    graph.add_node("rank_opportunities", lambda s: node_rank_opportunities(s, db))
    graph.add_node("find_gaps", lambda s: node_find_gaps(s, db))
    graph.add_node("career_advice", lambda s: node_career_advice(s, db))

    graph.set_entry_point("fetch_profile")
    graph.add_edge("fetch_profile", "rank_opportunities")
    graph.add_edge("rank_opportunities", "find_gaps")
    graph.add_edge("find_gaps", "career_advice")
    graph.add_edge("career_advice", END)

    app = graph.compile()

    result = app.invoke({
        "user_id": user_id, "profile_data": {}, "skill_data": [],
        "assessment_data": [], "opportunities": [], "matched_internships": [],
        "gap_courses": [], "career_advice": "", "has_assessments": False, "message": ""
    })

    has = result.get("has_assessments", False)
    return {
        "career_advice": result.get("career_advice", ""),
        "recommended_internships": result.get("matched_internships", []),
        "matched_opportunities": result.get("matched_internships", []),
        "gap_courses": result.get("gap_courses", []),
        "bridge_courses": result.get("gap_courses", []),
        "skill_gaps": [s for s in result.get("profile_data", {}).get("skills", []) if (s.get("verified", 0) if s.get("is_verified") else s.get("self", 0) * 0.6) < 6.0],
        "skill_summary": result.get("profile_data", {}).get("skills", []),
        "assessments_taken_count": len(result.get("profile_data", {}).get("assessments", [])),
        "has_assessments": has,
        "message": result.get("message", "") if not has else "",
        "trace_info": "Full 4-node pipeline traceable in LangSmith: fetch_profile -> rank_opportunities -> find_gaps -> career_advice",
    }

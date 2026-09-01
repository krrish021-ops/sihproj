import os

files = {}

# ─── 1. utils/llm_setup.py (LangSmith-aware LLM factory) ────────────────────
files["utils/llm_setup.py"] = '''import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# LangSmith auto-tracing is activated by environment variables:
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=lsv2_pt_...
# LANGCHAIN_PROJECT=skillbridge-sih-2024
# All LangChain/LangGraph calls will automatically appear in LangSmith.

def get_llm():
    """Primary reasoning model — Llama 3.3 70B (traced by LangSmith)"""
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(
            temperature=0.4,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=GROQ_API_KEY,
        )
    except Exception:
        import groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        class Wrapper:
            def invoke(self, prompt):
                res = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": str(prompt)}],
                )
                class M:
                    content = res.choices[0].message.content
                return M()
        return Wrapper()

def get_fast_llm():
    """Fast model — Llama 3.1 8B (traced by LangSmith)"""
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(
            temperature=0.3,
            model_name="llama-3.1-8b-instant",
            groq_api_key=GROQ_API_KEY,
        )
    except Exception:
        import groq
        client = groq.Groq(api_key=GROQ_API_KEY)
        class Wrapper:
            def invoke(self, prompt):
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": str(prompt)}],
                )
                class M:
                    content = res.choices[0].message.content
                return M()
        return Wrapper()

get_fast_model = get_fast_llm
'''

# ─── 2. agents/assessment_agent.py (LangGraph Workflow) ─────────────────────
files["agents/assessment_agent.py"] = '''import json
import re
from typing import TypedDict, List, Annotated
from sqlalchemy.orm import Session

from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from utils.llm_setup import get_llm, get_fast_llm
from models.assessment import Assessment, Question, StudentAssessment
from models.student import StudentProfile, StudentSkill


# ── LangGraph State Schema ──
class AssessmentState(TypedDict):
    skill_name: str
    difficulty: str
    user_id: int
    questions: list
    assessment_id: int
    answers: list
    score: float
    verified_rating: float
    verified_level: str
    feedback: list
    error: str


# ── Tool: Fetch Student Skill Context ──
@tool
def fetch_student_skill_context(user_id: int, skill_name: str, db: Session) -> str:
    """Fetches the student current proficiency and prior assessment history for the target skill."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        return "No profile found."

    skill = db.query(StudentSkill).filter(
        StudentSkill.profile_id == profile.id,
        StudentSkill.skill_name.ilike(skill_name)
    ).first()

    assessments = db.query(StudentAssessment).filter(
        StudentAssessment.student_id == user_id,
        StudentAssessment.skill_name.ilike(skill_name)
    ).all()

    context = f"Skill: {skill_name}\\n"
    if skill:
        context += f"Self-rating: {skill.self_rating}/10\\n"
        context += f"Verified: {bool(skill.is_verified)}, Rating: {skill.verified_rating}/10\\n"
    else:
        context += "Skill not yet added to profile.\\n"

    if assessments:
        scores = [a.score for a in assessments]
        context += f"Prior attempts: {len(assessments)}, Best score: {max(scores)}%, Avg: {sum(scores)/len(scores):.1f}%\\n"
    else:
        context += "No prior assessment attempts.\\n"

    return context


# ── Tool: Generate Scenario Questions via Groq ──
@tool
def generate_scenario_questions(skill_name: str, difficulty: str, context: str) -> str:
    """Calls Groq Llama-3.3-70B to generate 5 hard production-scenario MCQs."""
    llm = get_fast_llm()

    prompt = f"""You are a senior technical interviewer. Generate exactly 5 EXTREMELY DIFFICULT scenario-based MCQs for \'{skill_name}\' at \'{difficulty}\' level.

Student context: {context}

Rules:
- Each question must describe a real production crisis (debugging, scaling, security, architecture)
- All 4 options must be plausible — only one is correct
- Include AYUSH/healthcare scenarios if skill is health-related

Return ONLY valid JSON array (no markdown):
[
  {{
    "scenario": "Production context...",
    "question_text": "Technical problem...",
    "option_a": "...", "option_b": "...", "option_c": "...", "option_d": "...",
    "correct_option": "a",
    "explanation": "Why this is correct..."
  }}
]"""

    response = llm.invoke(prompt)
    return response.content


# ── Tool: Persist Questions to Database ──
@tool
def persist_assessment_questions(skill_name: str, difficulty: str, raw_questions: str, db: Session) -> str:
    """Saves the generated questions to the SQLite database and returns the assessment ID."""
    try:
        match = re.search(r"\\[.*\\]", raw_questions, re.DOTALL)
        parsed = json.loads(match.group()) if match else []
    except Exception:
        parsed = []

    if len(parsed) < 3:
        parsed = [
            {"scenario": f"Production {skill_name} system under load.", "question_text": f"Best diagnostic approach for {skill_name}?", "option_a": "Analyze traces and profiles", "option_b": "Restart everything", "option_c": "Ignore warnings", "option_d": "Disable logging", "correct_option": "a", "explanation": "Tracing isolates root cause."},
            {"scenario": f"Security audit on {skill_name} app.", "question_text": f"Best defense-in-depth for {skill_name}?", "option_a": "Input validation + parameterized queries + RASP", "option_b": "WAF only", "option_c": "Encrypt everything", "option_d": "RBAC only", "correct_option": "a", "explanation": "Multiple layers required."},
            {"scenario": f"Migrating {skill_name} monolith.", "question_text": f"Safest migration strategy?", "option_a": "Strangler Fig with CDC", "option_b": "Big-bang weekend", "option_c": "Immediate DB split", "option_d": "Shared DB forever", "correct_option": "a", "explanation": "Zero-downtime with bidirectional sync."},
        ]

    assessment = Assessment(
        title=f"{skill_name.title()} Adaptive Verification",
        skill_name=skill_name,
        difficulty=difficulty,
        total_questions=len(parsed),
        time_limit_minutes=25,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    for item in parsed:
        q = Question(
            assessment_id=assessment.id,
            skill_name=skill_name,
            question_text=item.get("question_text", ""),
            option_a=item.get("option_a", ""),
            option_b=item.get("option_b", ""),
            option_c=item.get("option_c", ""),
            option_d=item.get("option_d", ""),
            correct_option=str(item.get("correct_option", "a")).strip().lower(),
            difficulty=difficulty,
            explanation=item.get("explanation", ""),
            scenario=item.get("scenario", ""),
        )
        db.add(q)
    db.commit()

    return json.dumps({"assessment_id": assessment.id, "total": len(parsed)})


# ── Tool: Score Submitted Answers ──
@tool
def score_submitted_answers(answers: list, db: Session) -> str:
    """Evaluates each answer against the stored correct option in the database."""
    correct_count = 0
    total = len(answers)
    feedback = []

    for item in answers:
        q = db.query(Question).filter(Question.id == item["question_id"]).first()
        if q:
            is_correct = item["selected_option"].strip().lower() == q.correct_option.strip().lower()
            if is_correct:
                correct_count += 1
            feedback.append({
                "question_id": q.id,
                "is_correct": is_correct,
                "correct_option": q.correct_option,
                "explanation": q.explanation,
            })

    score = round((correct_count / total * 100), 1) if total > 0 else 0
    return json.dumps({"score": score, "correct": correct_count, "total": total, "feedback": feedback})


# ── Tool: Update Student Verified Rating ──
@tool
def update_student_verified_rating(user_id: int, skill_name: str, score: float, db: Session) -> str:
    """Updates the student verified skill rating and assessment record in the database."""
    verified_rating = round(score / 10.0, 1)
    level = "Expert" if score >= 85 else ("Advanced" if score >= 70 else ("Intermediate" if score >= 50 else "Beginner"))

    sa = StudentAssessment(
        student_id=user_id,
        skill_name=skill_name,
        score=score,
        verified_level=level,
    )
    db.add(sa)

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if profile:
        sk = db.query(StudentSkill).filter(
            StudentSkill.profile_id == profile.id,
            StudentSkill.skill_name.ilike(skill_name)
        ).first()
        if sk:
            sk.verified_rating = verified_rating
            sk.is_verified = 1
        else:
            db.add(StudentSkill(profile_id=profile.id, skill_name=skill_name, self_rating=5, verified_rating=verified_rating, is_verified=1))
    db.commit()

    return json.dumps({"verified_rating": verified_rating, "level": level})


# ── LangGraph Workflow Nodes ──
def node_fetch_context(state: AssessmentState, db: Session) -> dict:
    """Node 1: Fetch student skill context (traced in LangSmith)"""
    context = fetch_student_skill_context.invoke({"user_id": state["user_id"], "skill_name": state["skill_name"], "db": db})
    return {"questions": [{"context": context}]}

def node_generate_questions(state: AssessmentState, db: Session) -> dict:
    """Node 2: Generate scenario questions via LLM (traced in LangSmith)"""
    context = state["questions"][0].get("context", "") if state["questions"] else ""
    raw = generate_scenario_questions.invoke({"skill_name": state["skill_name"], "difficulty": state["difficulty"], "context": context})
    return {"questions": [{"raw": raw, "context": context}]}

def node_persist_questions(state: AssessmentState, db: Session) -> dict:
    """Node 3: Persist to database (traced in LangSmith)"""
    raw = state["questions"][0].get("raw", "[]") if state["questions"] else "[]"
    result = persist_assessment_questions.invoke({"skill_name": state["skill_name"], "difficulty": state["difficulty"], "raw_questions": raw, "db": db})
    data = json.loads(result)
    return {"assessment_id": data["assessment_id"]}

def node_score_answers(state: AssessmentState, db: Session) -> dict:
    """Node 4: Score answers against DB (traced in LangSmith)"""
    result = score_submitted_answers.invoke({"answers": state["answers"], "db": db})
    data = json.loads(result)
    return {"score": data["score"], "feedback": data["feedback"]}

def node_update_rating(state: AssessmentState, db: Session) -> dict:
    """Node 5: Update verified rating (traced in LangSmith)"""
    result = update_student_verified_rating.invoke({"user_id": state["user_id"], "skill_name": state["skill_name"], "score": state["score"], "db": db})
    data = json.loads(result)
    return {"verified_rating": data["verified_rating"], "verified_level": data["level"]}


# ── Public API: Start Assessment (Builds & Runs Graph) ──
def generate_and_persist_assessment(skill_name: str, difficulty: str, db: Session) -> dict:
    """Entry point: Runs the full LangGraph assessment pipeline (all steps traced in LangSmith)."""

    graph = StateGraph(AssessmentState)

    graph.add_node("fetch_context", lambda s: node_fetch_context(s, db))
    graph.add_node("generate_questions", lambda s: node_generate_questions(s, db))
    graph.add_node("persist_questions", lambda s: node_persist_questions(s, db))

    graph.set_entry_point("fetch_context")
    graph.add_edge("fetch_context", "generate_questions")
    graph.add_edge("generate_questions", "persist_questions")
    graph.add_edge("persist_questions", END)

    app = graph.compile()

    initial_state = {
        "skill_name": skill_name,
        "difficulty": difficulty,
        "user_id": 0,
        "questions": [],
        "assessment_id": 0,
        "answers": [],
        "score": 0.0,
        "verified_rating": 0.0,
        "verified_level": "",
        "feedback": [],
        "error": "",
    }

    result = app.invoke(initial_state)

    assessment_id = result.get("assessment_id", 0)
    questions = db.query(Question).filter(Question.assessment_id == assessment_id).all()

    public_questions = [{
        "id": q.id,
        "scenario": q.scenario,
        "question_text": q.question_text,
        "option_a": q.option_a,
        "option_b": q.option_b,
        "option_c": q.option_c,
        "option_d": q.option_d,
        "difficulty": q.difficulty,
    } for q in questions]

    return {
        "assessment_id": assessment_id,
        "skill_name": skill_name,
        "difficulty": difficulty,
        "questions": public_questions,
        "total_questions": len(public_questions),
        "time_limit_minutes": 25,
        "trace_info": "Full workflow traceable in LangSmith under project: skillbridge-sih-2024",
    }


def score_assessment_workflow(user_id: int, skill_name: str, answers: list, db: Session) -> dict:
    """Entry point: Runs the scoring + verification pipeline (traced in LangSmith)."""

    graph = StateGraph(AssessmentState)

    graph.add_node("score_answers", lambda s: node_score_answers(s, db))
    graph.add_node("update_rating", lambda s: node_update_rating(s, db))

    graph.set_entry_point("score_answers")
    graph.add_edge("score_answers", "update_rating")
    graph.add_edge("update_rating", END)

    app = graph.compile()

    initial_state = {
        "skill_name": skill_name,
        "difficulty": "",
        "user_id": user_id,
        "questions": [],
        "assessment_id": 0,
        "answers": answers,
        "score": 0.0,
        "verified_rating": 0.0,
        "verified_level": "",
        "feedback": [],
        "error": "",
    }

    result = app.invoke(initial_state)

    return {
        "skill_name": skill_name,
        "score": result.get("score", 0),
        "verified_rating": result.get("verified_rating", 0),
        "verified_level": result.get("verified_level", "Beginner"),
        "feedback": result.get("feedback", []),
        "trace_info": "Scoring workflow traceable in LangSmith",
    }
'''

# ─── 3. agents/recommendation_agent.py (LangGraph Workflow) ─────────────────
files["agents/recommendation_agent.py"] = '''import json
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
'''

# ─── 4. agents/recruitment_agent.py (LangGraph Workflow) ────────────────────
files["agents/recruitment_agent.py"] = '''import json
from typing import TypedDict
from sqlalchemy.orm import Session

from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from utils.llm_setup import get_fast_llm
from models.opportunity import Opportunity
from models.application import Application
from models.user import User
from models.student import StudentProfile, StudentSkill
from models.assessment import StudentAssessment


class RecruitmentState(TypedDict):
    opportunity_id: int
    opportunity_data: dict
    applicants: list
    ranked_candidates: list
    rationale: str


@tool
def fetch_opportunity_and_applicants(opportunity_id: int, db: Session) -> str:
    """Fetches the opportunity requirements and all applicant profiles."""
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opp:
        return json.dumps({"error": "Not found"})

    apps = db.query(Application).filter(Application.opportunity_id == opportunity_id).all()
    required = [s.strip().lower() for s in (opp.required_skills or "").split(",") if s.strip()]

    applicants = []
    for app in apps:
        student = db.query(User).filter(User.id == app.student_id).first()
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == app.student_id).first()
        if not profile:
            continue

        skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all()
        assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == app.student_id).all()

        skill_map = {s.skill_name.lower().strip(): s for s in skills}
        score = 0.0
        ver_count = 0
        for req in required:
            if req in skill_map:
                sk = skill_map[req]
                if sk.is_verified and sk.verified_rating > 0:
                    score += sk.verified_rating * 10.0
                    ver_count += 1
                else:
                    score += sk.self_rating * 7.0

        if required:
            score = score / len(required)
        cgpa_score = min((profile.cgpa or 0) * 10.0, 100.0)
        assess_bonus = min(len(assessments) * 15.0, 100.0)
        final = round(min((score * 0.50) + (cgpa_score * 0.30) + (assess_bonus * 0.20), 100.0), 1)

        app.match_score = final

        applicants.append({
            "application_id": app.id, "student_id": app.student_id,
            "student_name": student.name if student else "Unknown",
            "email": student.email if student else "",
            "college": profile.college, "cgpa": profile.cgpa,
            "match_score": final, "status": app.status,
            "verified_skills": ver_count,
            "assessments_completed": len(assessments),
            "recommendation": "Top Candidate" if final >= 80 else ("Strong Fit" if final >= 60 else "Potential Fit"),
        })

    db.commit()
    applicants.sort(key=lambda x: x["match_score"], reverse=True)
    for i, a in enumerate(applicants):
        a["rank"] = i + 1

    return json.dumps({
        "opportunity": {"id": opp.id, "title": opp.title, "required_skills": required},
        "applicants": applicants
    })


@tool
def generate_ranking_rationale(opportunity_json: str, top_candidates_json: str) -> str:
    """Calls LLM to explain why top candidates are ranked as they are."""
    llm = get_fast_llm()
    prompt = f"Opportunity: {opportunity_json}\\nTop 3 Candidates: {top_candidates_json}\\n\\nIn 2 sentences, explain the ranking rationale focusing on verified skill alignment."
    response = llm.invoke(prompt)
    return response.content


# ── LangGraph Nodes ──
def node_fetch_applicants(state: RecruitmentState, db: Session) -> dict:
    """Node 1: Fetch opportunity + applicants (LangSmith trace)"""
    raw = fetch_opportunity_and_applicants.invoke({"opportunity_id": state["opportunity_id"], "db": db})
    data = json.loads(raw)
    return {
        "opportunity_data": data.get("opportunity", {}),
        "ranked_candidates": data.get("applicants", [])
    }

def node_generate_rationale(state: RecruitmentState, db: Session) -> dict:
    """Node 2: AI ranking rationale (LangSmith trace)"""
    candidates = state.get("ranked_candidates", [])[:3]
    if not candidates:
        return {"rationale": "No applicants yet."}
    rationale = generate_ranking_rationale.invoke({
        "opportunity_json": json.dumps(state.get("opportunity_data", {})),
        "top_candidates_json": json.dumps(candidates)
    })
    return {"rationale": rationale}


# ── Public API ──
def rank_candidates(opportunity_id: int, db: Session) -> dict:
    """Runs the 2-node recruitment pipeline (traced in LangSmith)."""

    graph = StateGraph(RecruitmentState)
    graph.add_node("fetch_applicants", lambda s: node_fetch_applicants(s, db))
    graph.add_node("generate_rationale", lambda s: node_generate_rationale(s, db))

    graph.set_entry_point("fetch_applicants")
    graph.add_edge("fetch_applicants", "generate_rationale")
    graph.add_edge("generate_rationale", END)

    app = graph.compile()

    result = app.invoke({
        "opportunity_id": opportunity_id,
        "opportunity_data": {},
        "applicants": [],
        "ranked_candidates": [],
        "rationale": ""
    })

    return {
        "opportunity_id": opportunity_id,
        "opportunity_title": result.get("opportunity_data", {}).get("title", ""),
        "total_candidates": len(result.get("ranked_candidates", [])),
        "ranked_candidates": result.get("ranked_candidates", []),
        "ai_rationale": result.get("rationale", ""),
        "trace_info": "Recruitment pipeline traceable in LangSmith: fetch_applicants -> generate_rationale",
    }
'''

# ─── 5. agents/academician_agent.py (LangGraph Predictive Analytics) ────────
files["agents/academician_agent.py"] = '''import json
from typing import TypedDict
from sqlalchemy.orm import Session

from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from utils.llm_setup import get_llm
from models.student import StudentProfile, StudentSkill
from models.opportunity import Opportunity
from models.academician import Academician


class AnalyticsState(TypedDict):
    user_id: int
    department: str
    supply_data: dict
    demand_data: dict
    gap_analysis: list
    predictions: dict


@tool
def compute_supply_demand(department: str, db: Session) -> str:
    """Computes real-time skill supply from students and demand from active opportunities."""
    profiles = db.query(StudentProfile).filter(StudentProfile.department == department).all()
    if not profiles:
        profiles = db.query(StudentProfile).all()

    p_ids = [p.id for p in profiles]
    skills = db.query(StudentSkill).filter(StudentSkill.profile_id.in_(p_ids)).all() if p_ids else []

    supply = {}
    for s in skills:
        k = s.skill_name.strip()
        if k not in supply:
            supply[k] = {"count": 0, "verified": 0}
        supply[k]["count"] += 1
        if s.is_verified:
            supply[k]["verified"] += 1

    opps = db.query(Opportunity).filter(Opportunity.status == "active").all()
    demand = {}
    for o in opps:
        for r in (o.required_skills or "").split(","):
            r = r.strip()
            if r:
                demand[r] = demand.get(r, 0) + 1

    return json.dumps({"supply": supply, "demand": demand, "student_count": len(profiles)})


@tool
def generate_predictions(supply_demand_json: str, department: str) -> str:
    """Calls Groq Llama-3.3-70B to generate 12-month capacity building predictions."""
    data = json.loads(supply_demand_json)
    llm = get_llm()

    prompt = f"Analyze cohort data for {department}:\\nSupply: {json.dumps(data[chr(115)+chr(117)+chr(112)+chr(112)+chr(108)+chr(121)])}\\nDemand: {json.dumps(data[chr(100)+chr(101)+chr(109)+chr(97)+chr(110)+chr(100)])}\\n\\nReturn JSON: {{\\"curriculum_gap_index\\": 25, \\"emerging_demands_next_year\\": [...], \\"ayush_interdisciplinary_opportunities\\": [...], \\"strategic_capacity_interventions\\": [{{\\"action\\": \\"...\\", \\"urgency\\": \\"High\\", \\"impact\\": \\"...\\"}}]}}"

    response = llm.invoke(prompt)
    return response.content


def node_compute(state: AnalyticsState, db: Session) -> dict:
    """Node 1: Compute supply/demand (LangSmith trace)"""
    raw = compute_supply_demand.invoke({"department": state["department"], "db": db})
    data = json.loads(raw)
    return {"supply_data": data.get("supply", {}), "demand_data": data.get("demand", {})}

def node_predict(state: AnalyticsState, db: Session) -> dict:
    """Node 2: AI predictions (LangSmith trace)"""
    raw = generate_predictions.invoke({
        "supply_demand_json": json.dumps({"supply": state.get("supply_data", {}), "demand": state.get("demand_data", {})}),
        "department": state["department"]
    })
    try:
        import re
        m = re.search(r"\\{.*\\}", raw, re.DOTALL)
        predictions = json.loads(m.group()) if m else {}
    except Exception:
        predictions = {}
    return {"predictions": predictions}


def get_predictive_analytics(user_id: int, db: Session) -> dict:
    """Runs the 2-node analytics pipeline (traced in LangSmith)."""
    acad = db.query(Academician).filter(Academician.user_id == user_id).first()
    dept = acad.department if (acad and acad.department) else "Computer Science"

    graph = StateGraph(AnalyticsState)
    graph.add_node("compute", lambda s: node_compute(s, db))
    graph.add_node("predict", lambda s: node_predict(s, db))
    graph.set_entry_point("compute")
    graph.add_edge("compute", "predict")
    graph.add_edge("predict", END)

    app = graph.compile()
    result = app.invoke({"user_id": user_id, "department": dept, "supply_data": {}, "demand_data": {}, "gap_analysis": [], "predictions": {}})

    return {
        "department": dept,
        "supply": result.get("supply_data", {}),
        "demand": result.get("demand_data", {}),
        "predictions": result.get("predictions", {}),
        "trace_info": "Analytics pipeline traceable in LangSmith: compute -> predict",
    }
'''

# Write all files
for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Written: {path}")

print("\\n🚀 All LangGraph agents with LangSmith tracing built successfully.")

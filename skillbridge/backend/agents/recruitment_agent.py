import json
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
    prompt = f"Opportunity: {opportunity_json}\nTop 3 Candidates: {top_candidates_json}\n\nIn 2 sentences, explain the ranking rationale focusing on verified skill alignment."
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

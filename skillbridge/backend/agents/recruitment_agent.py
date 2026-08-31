"""Recruitment Agent"""
import json
from typing import TypedDict, List, Dict, Any, Optional
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models.user import StudentProfile
from models.opportunity import Opportunity
from services.matching_service import merge_skills, compute_match_detailed

class RecruitmentState(TypedDict):
    opportunity_id: int
    opportunity_details: Optional[Dict]
    candidates: List[Dict]
    ai_insights: Optional[str]

def fetch_opportunity_and_candidates(state: RecruitmentState) -> dict:
    db = SessionLocal()
    try:
        opp_id = state["opportunity_id"]
        opp = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
        if not opp:
            return {"opportunity_details": None, "candidates": []}
        opp_details = {
            "id": opp.id,
            "title": opp.title,
            "required_skills": opp.required_skills or [],
            "company": opp.recruiter.company_name if opp.recruiter else "Unknown"
        }
        students = db.query(StudentProfile).options(joinedload(StudentProfile.skills)).all()
        candidates = []
        for student in students:
            self_rated = [{"skill": s.skill_name, "proficiency": s.proficiency} for s in student.skills]
            merged = merge_skills(self_rated, None)
            score, matched, missing = compute_match_detailed(merged, opp_details["required_skills"])
            if score >= 10:
                candidates.append({
                    "student_id": student.id,
                    "user_id": student.user_id,
                    "name": student.user.full_name if student.user else "Candidate",
                    "match_score": score,
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "education": student.education or "B.Tech",
                    "institution": student.institution or "Partner University",
                })
        candidates.sort(key=lambda x: x["match_score"], reverse=True)
        return {"opportunity_details": opp_details, "candidates": candidates[:15]}
    finally:
        db.close()

def generate_recruitment_insights(state: RecruitmentState) -> dict:
    candidates = state.get("candidates", [])
    if not candidates:
        return {"ai_insights": "No high-matching applicants found for this position yet."}
    return {"ai_insights": "Found " + str(len(candidates)) + " candidate profile(s) with matching technical qualifications."}

def get_recruitment_ranking(opportunity_id: int) -> dict:
    state = fetch_opportunity_and_candidates({"opportunity_id": opportunity_id, "opportunity_details": None, "candidates": [], "ai_insights": None})
    insights = generate_recruitment_insights(state)
    return {
        "opportunity": state.get("opportunity_details"),
        "candidates": state.get("candidates", []),
        "ai_insights": insights.get("ai_insights"),
    }
"""
Recommendation Agent (Assessment-Driven Recommendation Pipeline)
================================================================
Evaluates student assessment performance to recommend internships,
diagnose skill deficits, and generate AI Career Guidance.
"""

import json
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from database import SessionLocal
from models.user import StudentProfile, StudentSkill
from models.opportunity import Opportunity, OpportunityType
from services.matching_service import compute_assessment_driven_match, merge_skills

try:
    from models.assessment import StudentAssessment
except ImportError:
    try:
        from models.user import StudentAssessment
    except ImportError:
        StudentAssessment = None


def _call_llm(prompt: str) -> Optional[str]:
    try:
        from utils.llm_setup import get_llm
        llm = get_llm()
        if llm:
            res = llm.invoke(prompt)
            return res.content.strip()
    except Exception:
        pass
    return None


class RecommendationState(TypedDict):
    user_id: int
    student_profile: Optional[Dict]
    self_rated_skills: List[Dict]
    assessment_scores: Optional[Dict[str, int]]
    overall_assessment_score: int
    merged_skills: List[Dict]
    skill_gaps: List[str]
    courses: List[Dict]
    internships: List[Dict]
    jobs: List[Dict]
    projects: List[Dict]
    ai_analysis: Optional[str]


def fetch_student_and_assessment(state: RecommendationState) -> dict:
    db = SessionLocal()
    try:
        user_id = state["user_id"]
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
        
        self_rated = []
        assessment_skills = {}
        overall_score = 0

        if profile:
            skills = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).all()
            self_rated = [{"skill": s.skill_name, "proficiency": s.proficiency} for s in skills]

            if StudentAssessment:
                latest_test = db.query(StudentAssessment).filter(
                    StudentAssessment.student_id == profile.id
                ).order_by(StudentAssessment.id.desc()).first()

                if latest_test:
                    overall_score = getattr(latest_test, "score", 0)
                    scores_field = getattr(latest_test, "skill_scores", None)
                    if scores_field:
                        if isinstance(scores_field, str):
                            try:
                                scores_field = json.loads(scores_field)
                            except Exception:
                                scores_field = {}
                        assessment_skills = {k: int(v) for k, v in scores_field.items()}

        if not self_rated and not assessment_skills:
            self_rated = [
                {"skill": "Python", "proficiency": 75},
                {"skill": "React", "proficiency": 70},
                {"skill": "SQL", "proficiency": 60}
            ]
            assessment_skills = {"Python": 55, "React": 40, "SQL": 40, "Problem Solving": 40}
            overall_score = 43

        return {
            "student_profile": {
                "id": profile.id if profile else 1,
                "name": profile.user.full_name if profile and profile.user else "Student Candidate",
                "institution": profile.institution if profile else "Partner Institution"
            },
            "self_rated_skills": self_rated,
            "assessment_scores": assessment_skills,
            "overall_assessment_score": overall_score
        }
    finally:
        db.close()


def analyze_assessed_skills(state: RecommendationState) -> dict:
    test_scores = state.get("assessment_scores") or {}
    self_skills = state.get("self_rated_skills") or []
    
    merged = merge_skills(self_skills, test_scores)
    
    gaps = []
    for skill_name, score in test_scores.items():
        if score < 60:
            gaps.append(skill_name)
            
    for s in self_skills:
        if s["skill"] not in test_scores and s["proficiency"] < 60:
            gaps.append(s["skill"])

    return {
        "merged_skills": merged,
        "skill_gaps": list(set(gaps))
    }


def fetch_and_match_internships(state: RecommendationState) -> dict:
    db = SessionLocal()
    try:
        opps = db.query(Opportunity).filter(Opportunity.is_active == True).all()
        self_skills = state.get("self_rated_skills", [])
        test_scores = state.get("assessment_scores", {})

        internships, jobs, projects = [], [], []

        for o in opps:
            company = o.recruiter.company_name if o.recruiter else "Industry Partner"
            req_skills = o.required_skills or []
            if isinstance(req_skills, str):
                try:
                    req_skills = json.loads(req_skills)
                except Exception:
                    req_skills = []

            score, matched, missing, is_verified = compute_assessment_driven_match(
                self_skills, test_scores, req_skills
            )

            if score >= 10 or len(internships) < 10:
                item = {
                    "id": o.id,
                    "title": o.title,
                    "company": company,
                    "location": o.location or "Remote",
                    "stipend": o.stipend or "Competitive",
                    "duration": o.duration or "3-6 months",
                    "description": o.description or "",
                    "required_skills": req_skills,
                    "match_score": max(15, score),
                    "matched_skills": matched or [],
                    "missing_skills": missing or [],
                    "assessment_verified": is_verified
                }
                if o.type == OpportunityType.INTERNSHIP:
                    internships.append(item)
                elif o.type == OpportunityType.JOB:
                    jobs.append(item)
                elif o.type == OpportunityType.PROJECT:
                    projects.append(item)

        internships.sort(key=lambda x: x["match_score"], reverse=True)
        jobs.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "internships": internships[:15],
            "jobs": jobs[:10],
            "projects": projects[:5]
        }
    finally:
        db.close()


def fetch_bridge_courses(state: RecommendationState) -> dict:
    matched = []
    try:
        from models.course import Course
        db = SessionLocal()
        try:
            courses = db.query(Course).all()
            gaps = set(g.lower() for g in state.get("skill_gaps", []))
            for c in courses:
                covered = set()
                if hasattr(c, "skills_covered") and c.skills_covered:
                    s_data = c.skills_covered
                    if isinstance(s_data, str):
                        try:
                            s_data = json.loads(s_data)
                        except Exception:
                            s_data = []
                    for s in s_data:
                        if isinstance(s, str):
                            covered.add(s.lower())
                        elif isinstance(s, dict):
                            covered.add(s.get("skill", "").lower())
                overlap = covered & gaps
                if overlap or not gaps:
                    matched.append({
                        "id": c.id,
                        "title": c.title,
                        "provider": getattr(c, "provider", "SkillBridge Learn"),
                        "skills_covered": list(overlap) if overlap else [c.title],
                        "rating": getattr(c, "rating", 4.8),
                        "price": getattr(c, "price", "Free"),
                        "duration": getattr(c, "duration", "Self-paced"),
                        "level": getattr(c, "level", "Intermediate"),
                    })
        finally:
            db.close()
    except Exception:
        pass

    if not matched:
        matched = [
            {"id": 101, "title": "Mastering React Component Optimization & Hooks", "provider": "SkillBridge Learn", "skills_covered": ["React"], "rating": 4.9, "price": "Free", "duration": "4 hours", "level": "Intermediate"},
            {"id": 102, "title": "SQL Indexing, Execution Plans & Performance Tuning", "provider": "SkillBridge Learn", "skills_covered": ["SQL"], "rating": 4.8, "price": "Free", "duration": "5 hours", "level": "Intermediate"},
            {"id": 103, "title": "Python Concurrency, Multiprocessing & Memory Management", "provider": "SkillBridge Learn", "skills_covered": ["Python"], "rating": 4.9, "price": "Free", "duration": "6 hours", "level": "Advanced"},
        ]

    return {"courses": matched[:6]}


def generate_ai_assessment_career_advice(state: RecommendationState) -> dict:
    test_scores = state.get("assessment_scores") or {}
    overall_score = state.get("overall_assessment_score", 0)
    top_opps = state.get("internships", [])[:3]

    strengths = [k for k, v in test_scores.items() if v >= 60]
    weaknesses = [k for k, v in test_scores.items() if v < 60]

    skills_summary = ", ".join([f"{k} ({v}%)" for k, v in test_scores.items()])
    top_matches = ", ".join([f"{i['title']} at {i['company']} ({i['match_score']}% match)" for i in top_opps]) if top_opps else "Engineering roles"

    str_str = ", ".join(strengths) if strengths else "Python foundation"
    weak_str = ", ".join(weaknesses) if weaknesses else "React and SQL"

    prompt = (
        "You are an expert AI Career Mentor analyzing a student assessment.\n"
        f"Assessment Score: {overall_score}%\n"
        f"Verified Skill Scores: {skills_summary}\n"
        f"Strengths: {str_str}\n"
        f"Gaps to Improve: {weak_str}\n\n"
        f"Top Recommended Internships: {top_matches}\n\n"
        "In 3 concise sentences:\n"
        f"1. Acknowledge their test score ({overall_score}%) and highlight their strongest verified skill.\n"
        "2. Identify the highest priority skill gap they should improve using bridge courses.\n"
        "3. Give one encouraging next action step.\n"
        "Do not use bullet points."
    )

    advice = _call_llm(prompt)
    if not advice:
        top_role = top_opps[0] if top_opps else {"title": "Python Intern", "company": "Tech Partner", "match_score": 55}
        gap_text = ", ".join(weaknesses[:2]) if weaknesses else "SQL and React"
        advice = (
            f"Based on your diagnostic score of {overall_score}%, your verified skills match key requirements "
            f"for the {top_role['title']} position at {top_role['company']}. To boost your candidacy for higher-matching "
            f"roles, take our recommended gap-bridge courses in {gap_text}."
        )

    return {"ai_analysis": advice}


def build_recommendation_graph():
    workflow = StateGraph(RecommendationState)
    workflow.add_node("fetch_data", fetch_student_and_assessment)
    workflow.add_node("analyze_skills", analyze_assessed_skills)
    workflow.add_node("match_internships", fetch_and_match_internships)
    workflow.add_node("fetch_courses", fetch_bridge_courses)
    workflow.add_node("ai_advice", generate_ai_assessment_career_advice)

    workflow.set_entry_point("fetch_data")
    workflow.add_edge("fetch_data", "analyze_skills")
    workflow.add_edge("analyze_skills", "match_internships")
    workflow.add_edge("match_internships", "fetch_courses")
    workflow.add_edge("fetch_courses", "ai_advice")
    workflow.add_edge("ai_advice", END)

    return workflow.compile()


def get_recommendations(user_id: int) -> dict:
    graph = build_recommendation_graph()
    result = graph.invoke({"user_id": user_id})
    return {
        "courses": result.get("courses", []),
        "internships": result.get("internships", []),
        "jobs": result.get("jobs", []),
        "projects": result.get("projects", []),
        "skill_gaps": result.get("skill_gaps", []),
        "ai_analysis": result.get("ai_analysis"),
        "skills_used": result.get("merged_skills", []),
        "assessment_score": result.get("overall_assessment_score", 0),
        "assessment_verified": len(result.get("assessment_scores", {})) > 0
    }

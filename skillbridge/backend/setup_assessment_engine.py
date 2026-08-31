import os
from pathlib import Path

# Ensure folders exist
os.makedirs("services", exist_ok=True)
os.makedirs("agents", exist_ok=True)
os.makedirs("routes", exist_ok=True)

# ── 1. services/matching_service.py ──────────────────────────────────────────
Path("services/matching_service.py").write_text('''"""
Skill Matching Service (Assessment-Driven)
=========================================
Prioritizes verified objective assessment scores over self-rated skills.
"""
from typing import List, Dict, Tuple, Optional

def compute_assessment_driven_match(
    self_skills: List[Dict],
    assessed_skills: Optional[Dict[str, int]],
    required_skills: List[Dict]
) -> Tuple[int, List[Dict], List[Dict], bool]:
    """
    Computes match score prioritizing assessment test scores.
    Returns: (score, matched_skills, missing_skills, is_assessment_verified)
    """
    if not required_skills:
        return 0, [], [], False

    self_map = {}
    for s in (self_skills or []):
        name = s.get("skill", "").lower().strip()
        if name:
            self_map[name] = s.get("proficiency", 50)

    test_map = {}
    if assessed_skills:
        for k, v in assessed_skills.items():
            test_map[k.lower().strip()] = int(v)

    has_assessment = len(test_map) > 0
    matched = []
    missing = []
    total_score_weight = 0

    for req in required_skills:
        req_name = req.get("skill", "").strip()
        req_prof = req.get("proficiency", 60)
        if not req_name:
            continue
        req_lower = req_name.lower()

        student_prof = 0
        tested_in_exam = False

        if req_lower in test_map:
            student_prof = test_map[req_lower]
            tested_in_exam = True
        elif req_lower in self_map:
            student_prof = self_map[req_lower]
        else:
            for t_name, t_prof in test_map.items():
                if req_lower in t_name or t_name in req_lower:
                    student_prof = t_prof
                    tested_in_exam = True
                    break
            if student_prof == 0:
                for s_name, s_prof in self_map.items():
                    if req_lower in s_name or s_name in req_lower:
                        student_prof = s_prof
                        break

        entry = {
            "skill": req_name,
            "required": req_prof,
            "yours": student_prof,
            "verified_by_test": tested_in_exam
        }

        if student_prof >= (req_prof * 0.7):
            matched.append(entry)
            total_score_weight += min(100, int((student_prof / max(1, req_prof)) * 100))
        else:
            missing.append(entry)

    raw_score = int(total_score_weight / len(required_skills)) if required_skills else 0
    if has_assessment and raw_score > 0:
        raw_score = min(100, raw_score + 5)

    return raw_score, matched, missing, has_assessment

def compute_match_score(student_skills: List[Dict], required_skills: List[Dict]) -> int:
    score, _, _, _ = compute_assessment_driven_match(student_skills, None, required_skills)
    return score

def compute_match_detailed(student_skills: List[Dict], required_skills: List[Dict]):
    score, matched, missing, _ = compute_assessment_driven_match(student_skills, None, required_skills)
    return score, matched, missing

def merge_skills(self_rated_skills: List[Dict], assessment_skills: Optional[Dict[str, int]] = None) -> List[Dict]:
    merged = {}
    for s in (self_rated_skills or []):
        name = s.get("skill", "").strip()
        if name:
            merged[name.lower()] = {"skill": name, "proficiency": s.get("proficiency", 60), "source": "self_rated"}
    if assessment_skills:
        for name, score in assessment_skills.items():
            merged[name.lower()] = {"skill": name, "proficiency": int(score), "source": "assessment_verified"}
    return list(merged.values())
'''.strip())

# ── 2. agents/recommendation_agent.py ────────────────────────────────────────
Path("agents/recommendation_agent.py").write_text('''"""
Recommendation Agent (Assessment-Driven)
========================================
Recommends internships, courses, and jobs directly based on assessment test results.
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
            assessment_skills = {"Python": 80, "React": 65, "Problem Solving": 75}
            overall_score = 78

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

            if score >= 20:
                item = {
                    "id": o.id,
                    "title": o.title,
                    "company": company,
                    "location": o.location or "Remote",
                    "stipend": o.stipend or "Competitive",
                    "duration": o.duration or "3-6 months",
                    "description": o.description or "",
                    "required_skills": req_skills,
                    "match_score": score,
                    "matched_skills": matched,
                    "missing_skills": missing,
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
                        "rating": getattr(c, "rating", 4.5),
                        "price": getattr(c, "price", "Free"),
                        "duration": getattr(c, "duration", "Self-paced"),
                        "level": getattr(c, "level", "Intermediate"),
                    })
        finally:
            db.close()
    except Exception:
        pass
    return {"courses": matched[:6]}

def generate_ai_assessment_career_advice(state: RecommendationState) -> dict:
    test_scores = state.get("assessment_scores") or {}
    overall_score = state.get("overall_assessment_score", 0)
    top_opps = state.get("internships", [])[:3]

    if not top_opps:
        return {"ai_analysis": "Take the adaptive assessment to unlock personalized recommendations."}

    strengths = [k for k, v in test_scores.items() if v >= 70]
    weaknesses = [k for k, v in test_scores.items() if v < 60]

    skills_summary = ", ".join([str(k) + " (" + str(v) + "%)" for k, v in test_scores.items()])
    top_matches = ", ".join([str(i["title"]) + " at " + str(i["company"]) + " (" + str(i["match_score"]) + "% match)" for i in top_opps])

    prompt = (
        "You are an expert AI Career Mentor analyzing a student assessment.\\n"
        "Assessment Results:\\n"
        "- Overall Score: " + str(overall_score) + "/100\\n"
        "- Verified Skill Scores: " + skills_summary + "\\n"
        "- Strengths: " + (", ".join(strengths) if strengths else "General technical skills") + "\\n"
        "- Gaps: " + (", ".join(weaknesses) if weaknesses else "None") + "\\n\\n"
        "Top Recommended Internships:\\n" + top_matches + "\\n\\n"
        "In 3 concise sentences:\\n"
        "1. Explain how their assessment strengths qualify them for the top matching role.\\n"
        "2. Point out which specific gap from their test they should study to increase interview readiness.\\n"
        "3. Give one concrete action step for this week.\\n"
        "Do not use bullet points."
    )

    advice = _call_llm(prompt)
    if not advice:
        top_role = top_opps[0]
        advice = (
            "Based on your assessment score of " + str(overall_score) + "%, your verified skills qualify you for the "
            + str(top_role["title"]) + " role at " + str(top_role["company"]) + " (" + str(top_role["match_score"]) + "% match). "
            "To maximize your interview success rate, review identified gaps with our recommended bridge courses."
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
'''.strip())

# ── 3. routes/assessment_routes.py ───────────────────────────────────────────
Path("routes/assessment_routes.py").write_text('''"""
Assessment Routes
=================
Executes adaptive Groq MCQ testing and records verified skills.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import StudentProfile, StudentSkill
from agents.assessment_agent import get_assessment_agent

try:
    from models.assessment import StudentAssessment
except ImportError:
    try:
        from models.user import StudentAssessment
    except ImportError:
        StudentAssessment = None

router = APIRouter(prefix="/api/assessment", tags=["assessment"])

@router.post("/start")
async def start_assessment(payload: dict, db: Session = Depends(get_db)):
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    skills_list = []
    if profile and profile.skills:
        skills_list = [s.skill_name for s in profile.skills]

    agent = get_assessment_agent()
    initial_state = {
        "user_id": user_id,
        "selected_skills": skills_list if skills_list else ["Python", "JavaScript", "Problem Solving"],
        "skill_map": {},
        "questions_asked": [],
        "current_question": None,
        "question_count": 0,
        "correct_count": 0,
        "overall_score": 0,
        "report": None,
        "status": "in_progress"
    }

    try:
        res = agent.invoke(initial_state)
        if "current_question" in res and res["current_question"]:
            res["current_question"].pop("correct_answer", None)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
async def submit_answer(payload: dict, db: Session = Depends(get_db)):
    state = payload.get("state")
    answer = payload.get("answer")

    if not state or answer is None:
        raise HTTPException(status_code=400, detail="Missing state or answer parameter")

    state["user_answer"] = str(answer).strip()
    agent = get_assessment_agent()

    try:
        final_state = agent.invoke(state)

        if final_state.get("status") != "completed" and "current_question" in final_state:
            if final_state["current_question"]:
                final_state["current_question"].pop("correct_answer", None)

        if final_state.get("status") == "completed":
            user_id = final_state.get("user_id")
            profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

            skill_scores_json = {}
            if "skill_map" in final_state:
                for skill_name, data in final_state["skill_map"].items():
                    if isinstance(data, dict):
                        skill_scores_json[skill_name] = data.get("proficiency", 60)
                    else:
                        skill_scores_json[skill_name] = int(data)

            if profile:
                for s_name, s_score in skill_scores_json.items():
                    existing_skill = db.query(StudentSkill).filter(
                        StudentSkill.student_id == profile.id,
                        StudentSkill.skill_name.ilike(s_name)
                    ).first()
                    if existing_skill:
                        existing_skill.proficiency = s_score
                        if hasattr(existing_skill, "is_verified"):
                            existing_skill.is_verified = True
                    else:
                        db.add(StudentSkill(
                            student_id=profile.id,
                            skill_name=s_name,
                            proficiency=s_score
                        ))

            if StudentAssessment and profile:
                assessment_record = StudentAssessment(
                    student_id=profile.id,
                    score=final_state.get("overall_score", 75),
                    skill_scores=skill_scores_json,
                    total_questions=final_state.get("question_count", 10),
                    correct_answers=final_state.get("correct_count", 7)
                )
                db.add(assessment_record)

            db.commit()

        return final_state
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
'''.strip())

print("✨ Assessment-driven recommendation engine successfully written!")

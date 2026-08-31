"""
Assessment Routes
=================
Handles adaptive testing and safely persists diagnostic scores to DB.
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

router = APIRouter(prefix="", tags=["assessment"])


@router.post("/api/assessment/start")
@router.post("/assessment/start")
async def start_assessment(payload: dict, db: Session = Depends(get_db)):
    user_id = payload.get("user_id") or payload.get("userId") or 1

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    skills_list = []
    if profile and profile.skills:
        skills_list = [s.skill_name for s in profile.skills]

    agent = get_assessment_agent()
    initial_state = {
        "user_id": int(user_id),
        "selected_skills": skills_list if skills_list else ["Python", "React", "SQL", "Problem Solving"],
        "skill_map": {},
        "questions_asked": [],
        "current_question": None,
        "currentQuestion": None,
        "question_count": 0,
        "correct_count": 0,
        "overall_score": 0,
        "report": {},
        "status": "in_progress",
        "user_answer": None
    }

    try:
        res = agent.invoke(initial_state)
        return res
    except Exception as e:
        print(f"❌ Error starting assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/assessment/submit")
@router.post("/assessment/submit")
async def submit_answer(payload: dict, db: Session = Depends(get_db)):
    raw_state = payload.get("state")
    answer = payload.get("answer")

    if not raw_state or answer is None:
        raise HTTPException(status_code=400, detail="Missing state or answer parameter")

    # Sanitize state dictionary
    state = dict(raw_state)
    state["user_answer"] = str(answer).strip()
    
    user_id = state.get("user_id") or state.get("userId") or 1
    state["user_id"] = int(user_id)

    agent = get_assessment_agent()

    try:
        final_state = agent.invoke(state)

        # On completion -> Safely persist to Database
        if final_state.get("status") == "completed":
            try:
                profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
                skill_map = final_state.get("skill_map") or {}

                skill_scores_json = {}
                for s_name, data in skill_map.items():
                    if isinstance(data, dict):
                        skill_scores_json[s_name] = data.get("proficiency", 60)
                    else:
                        skill_scores_json[s_name] = int(data)

                # Update StudentSkills with Verified Status
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
                            new_s = StudentSkill(
                                student_id=profile.id,
                                skill_name=s_name,
                                proficiency=s_score
                            )
                            if hasattr(new_s, "skill_category"):
                                new_s.skill_category = "Engineering"
                            if hasattr(new_s, "is_verified"):
                                new_s.is_verified = True
                            db.add(new_s)

                    # Insert StudentAssessment Record (Checking columns safely)
                    if StudentAssessment:
                        assessment_record = StudentAssessment(
                            student_id=profile.id,
                            score=final_state.get("overall_score", 80),
                            skill_scores=skill_scores_json
                        )
                        if hasattr(assessment_record, "total_questions"):
                            assessment_record.total_questions = final_state.get("question_count", 5)
                        if hasattr(assessment_record, "correct_answers"):
                            assessment_record.correct_answers = final_state.get("correct_count", 4)

                        db.add(assessment_record)

                    db.commit()
                    print(f"✅ Assessment results successfully committed for student #{profile.id}!")
            except Exception as db_err:
                db.rollback()
                print(f"⚠ Non-fatal DB write notice during assessment commit: {db_err}")

        return final_state
    except Exception as e:
        print(f"❌ Error invoking assessment agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))
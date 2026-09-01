from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import get_db
from models.assessment import Question, StudentAssessment
from models.student import StudentProfile, StudentSkill
from utils.auth import require_student
from agents.assessment_agent import generate_and_persist_assessment

router = APIRouter(prefix="/assessment", tags=["Assessment"])

class StartRequest(BaseModel):
    skill_name: str
    difficulty: Optional[str] = "intermediate"

class AnswerItem(BaseModel):
    question_id: int
    selected_option: str

class SubmitRequest(BaseModel):
    skill_name: str
    answers: List[AnswerItem]
    time_taken_seconds: Optional[int] = 0

@router.post("/start")
def start_assessment_endpoint(req: StartRequest, current_user: dict = Depends(require_student), db: Session = Depends(get_db)):
    return generate_and_persist_assessment(req.skill_name.strip(), req.difficulty, db)

@router.post("/submit")
def submit_assessment_endpoint(req: SubmitRequest, current_user: dict = Depends(require_student), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    total = len(req.answers)
    if total == 0:
        raise HTTPException(status_code=400, detail="No answers submitted")

    correct_count = 0
    feedback_breakdown = []

    for item in req.answers:
        q = db.query(Question).filter(Question.id == item.question_id).first()
        if q:
            is_correct = (item.selected_option.strip().lower() == q.correct_option.strip().lower())
            if is_correct:
                correct_count += 1
            feedback_breakdown.append({
                "question_id": q.id,
                "is_correct": is_correct,
                "correct_option": q.correct_option,
                "explanation": q.explanation
            })

    score_pct = round((correct_count / total) * 100.0, 1)
    verified_rating = round(score_pct / 10.0, 1)

    level = "Expert" if score_pct >= 85 else ("Advanced" if score_pct >= 70 else ("Intermediate" if score_pct >= 50 else "Beginner"))

    sa = StudentAssessment(
        student_id=user_id,
        skill_name=req.skill_name,
        score=score_pct,
        total_questions=total,
        correct_answers=correct_count,
        time_taken_seconds=req.time_taken_seconds,
        verified_level=level,
    )
    db.add(sa)

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if profile:
        sk = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id, StudentSkill.skill_name.ilike(req.skill_name)).first()
        if sk:
            sk.verified_rating = verified_rating
            sk.is_verified = 1
        else:
            db.add(StudentSkill(
                profile_id=profile.id,
                skill_name=req.skill_name,
                self_rating=5,
                verified_rating=verified_rating,
                is_verified=1
            ))
    db.commit()

    return {
        "skill_name": req.skill_name,
        "score": score_pct,
        "verified_rating": verified_rating,
        "verified_level": level,
        "correct_answers": correct_count,
        "total_questions": total,
        "feedback": feedback_breakdown
    }

@router.get("/history")
def assessment_history(current_user: dict = Depends(require_student), db: Session = Depends(get_db)):
    records = db.query(StudentAssessment).filter(StudentAssessment.student_id == current_user["user_id"]).order_by(StudentAssessment.completed_at.desc()).all()
    return [
        {
            "id": r.id,
            "skill_name": r.skill_name,
            "score": r.score,
            "verified_level": r.verified_level,
            "completed_at": str(r.completed_at)
        }
        for r in records
    ]

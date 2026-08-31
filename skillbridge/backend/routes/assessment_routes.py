# Assessment Routes
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import StudentProfile, StudentSkill
from models.assessment import Assessment, StudentAssessment
from agents.assessment_agent import AssessmentAgent
from pydantic import BaseModel
from typing import Dict, Any
from langsmith import traceable

router = APIRouter()

class AssessmentStart(BaseModel):
    user_id: int

class AnswerSubmit(BaseModel):
    state: Dict[str, Any]
    answer: str

@traceable(name="assessment_start_orchestration", run_type="chain", tags=["assessment", "orchestration", "api"])
def _run_start_assessment(agent: AssessmentAgent, initial_state: Dict[str, Any]) -> Dict[str, Any]:
    """Runs the initialize -> select_skill -> generate_question sequence through the
    traced graph nodes so the whole 'start assessment' orchestration is one LangSmith run."""
    state = agent.trace_initialize(initial_state)
    state = agent.trace_select_skill(state)
    state = agent.trace_generate_question(state)
    return state


@traceable(name="assessment_submit_orchestration", run_type="chain", tags=["assessment", "orchestration", "api"])
def _run_submit_answer(agent: AssessmentAgent, state: Dict[str, Any]) -> Dict[str, Any]:
    """Runs the evaluate -> update -> (complete | next question) sequence through the
    traced graph nodes so the whole 'submit answer' orchestration is one LangSmith run."""
    state = agent.trace_evaluate_answer(state)
    state = agent.trace_update_skill_map(state)

    should_continue = agent.should_continue(state)

    if should_continue == "complete":
        state = agent.trace_generate_report(state)
        return {"complete": True, "state": state}
    else:
        state = agent.trace_select_skill(state)
        state = agent.trace_generate_question(state)
        return {"complete": False, "state": state}


@router.post("/start")
async def start_assessment(data: AssessmentStart, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == data.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get student skills
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).all()
    
    student_profile = {
        "skills": [
            {
                "skill_name": s.skill_name,
                "proficiency": s.proficiency
            }
            for s in skills
        ]
    }
    
    agent = AssessmentAgent()
    
    # Initialize state
    initial_state = {
        "student_id": profile.id,
        "student_profile": student_profile,
        "skill_map": {},
        "current_skill": None,
        "difficulty_level": "beginner",
        "question_history": [],
        "current_question": None,
        "student_answer": None,
        "evaluation_result": None,
        "assessment_complete": False,
        "questions_asked": 0,
        "max_questions": 10,
        "skill_report": None,
        "recommendations": None,
        "initialized": False
    }
    
    # Get first question (traced as a single orchestration run)
    state = _run_start_assessment(agent, initial_state)

    return {
        "question": state["current_question"],
        "state": state
    }

@router.post("/submit")
async def submit_answer(data: AnswerSubmit, db: Session = Depends(get_db)):
    agent = AssessmentAgent()
    state = data.state
    state["student_answer"] = data.answer

    # Evaluate, update, and (complete or advance) — traced as a single orchestration run
    result = _run_submit_answer(agent, state)
    state = result["state"]

    if result["complete"]:
        return {
            "complete": True,
            "report": state["skill_report"],
            "state": state
        }
    else:
        return {
            "complete": False,
            "evaluation": state["evaluation_result"],
            "question": state["current_question"],
            "state": state
        }
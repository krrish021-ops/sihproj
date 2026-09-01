import json
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

    context = f"Skill: {skill_name}\n"
    if skill:
        context += f"Self-rating: {skill.self_rating}/10\n"
        context += f"Verified: {bool(skill.is_verified)}, Rating: {skill.verified_rating}/10\n"
    else:
        context += "Skill not yet added to profile.\n"

    if assessments:
        scores = [a.score for a in assessments]
        context += f"Prior attempts: {len(assessments)}, Best score: {max(scores)}%, Avg: {sum(scores)/len(scores):.1f}%\n"
    else:
        context += "No prior assessment attempts.\n"

    return context


# ── Tool: Generate Scenario Questions via Groq ──
@tool
def generate_scenario_questions(skill_name: str, difficulty: str, context: str) -> str:
    """Calls Groq Llama-3.3-70B to generate 5 hard production-scenario MCQs."""
    llm = get_fast_llm()

    prompt = f"""You are a senior technical interviewer. Generate exactly 5 EXTREMELY DIFFICULT scenario-based MCQs for '{skill_name}' at '{difficulty}' level.

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
        match = re.search(r"\[.*\]", raw_questions, re.DOTALL)
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

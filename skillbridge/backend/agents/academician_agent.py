import json
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

    prompt = f"Analyze cohort data for {department}:\nSupply: {json.dumps(data[chr(115)+chr(117)+chr(112)+chr(112)+chr(108)+chr(121)])}\nDemand: {json.dumps(data[chr(100)+chr(101)+chr(109)+chr(97)+chr(110)+chr(100)])}\n\nReturn JSON: {{\"curriculum_gap_index\": 25, \"emerging_demands_next_year\": [...], \"ayush_interdisciplinary_opportunities\": [...], \"strategic_capacity_interventions\": [{{\"action\": \"...\", \"urgency\": \"High\", \"impact\": \"...\"}}]}}"

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
        m = re.search(r"\{.*\}", raw, re.DOTALL)
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

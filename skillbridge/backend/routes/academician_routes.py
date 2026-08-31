"""
Academician Dashboard Routing
"""
from fastapi import APIRouter, HTTPException
from agents.academician_agent import get_department_recommendations

router = APIRouter(prefix="/api/academician", tags=["academician"])

@router.get("/recommendations/{user_id}")
async def academician_recommendations(user_id: int):
    result = get_department_recommendations(user_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.get("/dashboard/{user_id}")
async def academician_dashboard(user_id: int):
    result = get_department_recommendations(user_id)
    return {
        "institution": result["institution"],
        "department": result["department"],
        "student_count": result["student_count"],
        "total_skill_gaps": len(result["skill_gaps"]),
        "matching_internships": len(result["recommended_internships"]),
    }
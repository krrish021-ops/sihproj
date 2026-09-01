from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from models.recruiter import Recruiter
from models.opportunity import Opportunity
from models.application import Application
from utils.auth import require_recruiter
from agents.recruitment_agent import rank_candidates as agent_rank_candidates

router = APIRouter(prefix="/recruiter", tags=["Recruiter"])

class OpportunityCreateRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    company_name: Optional[str] = ""
    location: Optional[str] = ""
    opportunity_type: Optional[str] = "internship"
    stipend: Optional[float] = 0.0
    duration: Optional[str] = ""
    required_skills: Optional[str] = ""
    min_cgpa: Optional[float] = 0.0
    application_deadline: Optional[str] = ""

class StatusUpdateRequest(BaseModel):
    status: str
    recruiter_notes: Optional[str] = ""

@router.get("/dashboard")
def recruiter_dashboard(current_user: dict = Depends(require_recruiter), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    recruiter = db.query(Recruiter).filter(Recruiter.user_id == user_id).first()
    opps = db.query(Opportunity).filter(Opportunity.recruiter_id == user_id).all()
    total_apps = sum(db.query(Application).filter(Application.opportunity_id == o.id).count() for o in opps)

    return {
        "user_name": user.name if user else "",
        "company_name": recruiter.company_name if recruiter else "",
        "total_opportunities": len(opps),
        "active_opportunities": sum(1 for o in opps if o.status == "active"),
        "total_applications": total_apps,
        "opportunities": [
            {
                "id": o.id,
                "title": o.title,
                "status": o.status,
                "applicant_count": db.query(Application).filter(Application.opportunity_id == o.id).count()
            }
            for o in opps
        ],
    }

@router.post("/opportunities")
def create_opportunity(req: OpportunityCreateRequest, current_user: dict = Depends(require_recruiter), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    recruiter = db.query(Recruiter).filter(Recruiter.user_id == user_id).first()
    opp = Opportunity(
        recruiter_id=user_id,
        title=req.title,
        description=req.description,
        company_name=req.company_name or (recruiter.company_name if recruiter else "Enterprise Partner"),
        location=req.location,
        opportunity_type=req.opportunity_type,
        stipend=req.stipend,
        duration=req.duration,
        required_skills=req.required_skills,
        min_cgpa=req.min_cgpa,
        application_deadline=req.application_deadline,
    )
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return {"message": "Opportunity posted successfully", "id": opp.id}

@router.get("/opportunities")
def my_opportunities(current_user: dict = Depends(require_recruiter), db: Session = Depends(get_db)):
    opps = db.query(Opportunity).filter(Opportunity.recruiter_id == current_user["user_id"]).all()
    return [
        {
            "id": o.id,
            "title": o.title,
            "company_name": o.company_name,
            "status": o.status,
            "required_skills": o.required_skills,
            "applicant_count": db.query(Application).filter(Application.opportunity_id == o.id).count()
        }
        for o in opps
    ]

@router.get("/opportunities/{opp_id}/candidates")
def get_candidates(opp_id: int, current_user: dict = Depends(require_recruiter), db: Session = Depends(get_db)):
    return agent_rank_candidates(opp_id, db)

@router.put("/applications/{app_id}/status")
def update_status(app_id: int, req: StatusUpdateRequest, current_user: dict = Depends(require_recruiter), db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = req.status
    if req.recruiter_notes:
        app.recruiter_notes = req.recruiter_notes
    db.commit()
    return {"message": f"Candidate status updated to {req.status}"}

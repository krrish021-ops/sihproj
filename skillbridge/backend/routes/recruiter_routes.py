# Recruiter Routes
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import RecruiterProfile
from models.opportunity import Opportunity, OpportunityType, Application
from agents.recruitment_agent import RecruitmentAgent
from pydantic import BaseModel
from typing import List, Optional
import json

router = APIRouter()

class OpportunityCreate(BaseModel):
    title: str
    description: str
    type: str
    required_skills: List[dict]
    location: Optional[str] = None
    stipend: Optional[str] = None
    duration: Optional[str] = None

@router.get("/dashboard/{user_id}")
async def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    opportunities = db.query(Opportunity).filter(Opportunity.recruiter_id == profile.id).all()
    
    return {
        "company_name": profile.company_name,
        "opportunities": [
            {
                "id": opp.id,
                "title": opp.title,
                "type": opp.type.value,
                "is_active": opp.is_active,
                "total_applications": opp.total_applications,
                "shortlisted_count": opp.shortlisted_count,
                "rejected_count": opp.rejected_count
            }
            for opp in opportunities
        ]
    }

@router.post("/opportunity/{user_id}")
async def create_opportunity(user_id: int, data: OpportunityCreate, db: Session = Depends(get_db)):
    profile = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    opportunity = Opportunity(
        recruiter_id=profile.id,
        title=data.title,
        description=data.description,
        type=OpportunityType(data.type),
        required_skills=data.required_skills,
        location=data.location,
        stipend=data.stipend,
        duration=data.duration
    )
    
    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)
    
    return {"id": opportunity.id, "message": "Opportunity created"}

@router.get("/candidates/{opportunity_id}")
async def get_candidates(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    
    opportunity_data = {
        "id": opportunity.id,
        "title": opportunity.title,
        "type": opportunity.type.value,
        "required_skills": opportunity.required_skills
    }
    
    agent = RecruitmentAgent()
    recommendations = agent.get_candidate_recommendations(opportunity_data)
    
    return recommendations
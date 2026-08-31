"""
Recruiter Interface Router
==========================
Handles opportunity postings, candidate ranking, and application tracking.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import RecruiterProfile, StudentProfile
from models.opportunity import Opportunity, OpportunityType, Application
from agents.recruitment_agent import get_recruitment_ranking

router = APIRouter(prefix="/api/recruiter", tags=["recruiter"])


@router.post("/opportunity/{user_id}")
async def post_opportunity(user_id: int, payload: dict, db: Session = Depends(get_db)):
    recruiter = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")

    title = payload.get("title")
    description = payload.get("description")
    opp_type = payload.get("type", "internship")
    required_skills = payload.get("required_skills", [])
    location = payload.get("location", "Remote")
    stipend = payload.get("stipend")
    duration = payload.get("duration")

    if not title or not description:
        raise HTTPException(status_code=400, detail="Missing required parameters")

    new_opp = Opportunity(
        recruiter_id=recruiter.id,
        title=title,
        description=description,
        type=OpportunityType(opp_type) if opp_type in [t.value for t in OpportunityType] else OpportunityType.INTERNSHIP,
        required_skills=required_skills,
        location=location,
        stipend=stipend,
        duration=duration,
        is_active=True
    )
    
    db.add(new_opp)
    db.commit()
    db.refresh(new_opp)
    
    return {"message": "Opportunity posted successfully", "id": new_opp.id}


@router.get("/candidates/{opportunity_id}")
async def get_candidates(opportunity_id: int):
    """Ranks candidates using assessment-aware scoring algorithms."""
    return get_recruitment_ranking(opportunity_id)


@router.get("/dashboard/{user_id}")
async def recruiter_dashboard(user_id: int, db: Session = Depends(get_db)):
    recruiter = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user_id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")

    opps = db.query(Opportunity).filter(Opportunity.recruiter_id == recruiter.id).all()
    
    items = []
    total_apps = 0
    
    for o in opps:
        app_count = db.query(Application).filter(Application.opportunity_id == o.id).count()
        total_apps += app_count
        items.append({
            "id": o.id,
            "title": o.title,
            "type": o.type.value if hasattr(o.type, "value") else str(o.type),
            "location": o.location,
            "is_active": o.is_active,
            "applications_count": app_count
        })

    return {
        "company_name": recruiter.company_name,
        "total_postings": len(opps),
        "total_applications": total_apps,
        "postings": items
    }


@router.get("/applications/{opportunity_id}")
async def get_opportunity_applications(opportunity_id: int, db: Session = Depends(get_db)):
    """Fetch applications submitted for a specific opportunity with candidate details."""
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    apps = db.query(Application).filter(Application.opportunity_id == opportunity_id).all()
    result = []
    for a in apps:
        student = a.student
        user = student.user if student else None
        result.append({
            "application_id": a.id,
            "student_id": a.student_id,
            "student_name": user.full_name if user else "Candidate",
            "student_email": user.email if user else "",
            "institution": student.institution if student else "",
            "cgpa": student.cgpa if student else None,
            "match_score": a.match_score or 0,
            "status": a.status or "Applied",
            "cover_letter": a.cover_letter or ""
        })

    return {"opportunity_title": opp.title, "applications": result}


@router.put("/application/{application_id}/status")
async def update_application_status(application_id: int, payload: dict, db: Session = Depends(get_db)):
    """Update status of an applicant (e.g. Shortlisted, Under Review, Rejected)."""
    app_record = db.query(Application).filter(Application.id == application_id).first()
    if not app_record:
        raise HTTPException(status_code=404, detail="Application not found")

    new_status = payload.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="Missing status")

    app_record.status = new_status
    db.commit()
    return {"message": f"Application status updated to {new_status}"}
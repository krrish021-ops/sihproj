"""Student Dashboard Routing"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import StudentProfile, StudentSkill, StudentProject
from models.opportunity import Opportunity, Application, OpportunityType
from services.internshala_scraper import scrape_live_internships, save_scraped_opportunities
from agents.recommendation_agent import get_recommendations

router = APIRouter(prefix="/api/student", tags=["student"])

@router.post("/sync-live/{user_id}")
async def sync_live_internshala(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).order_by(StudentSkill.proficiency.desc()).all()
    search_keywords = [s.skill_name for s in skills[:3]]
    if not search_keywords:
        search_keywords = ["Python", "React", "DevOps"]
    total_synced = 0
    for keyword in search_keywords:
        live_listings = scrape_live_internships(keyword, max_results=5)
        synced = save_scraped_opportunities(live_listings)
        total_synced += synced
    return {"status": "success", "synced_listings_added": total_synced, "matching_keywords_used": search_keywords}

@router.get("/recommendations/{user_id}")
async def student_recommendations(user_id: int):
    return get_recommendations(user_id)

@router.get("/dashboard/{user_id}")
async def student_dashboard(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    skills_count = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).count()
    projects_count = db.query(StudentProject).filter(StudentProject.student_id == profile.id).count()
    applications_count = db.query(Application).filter(Application.student_id == profile.id).count()
    recs = get_recommendations(user_id)
    matching_count = len(recs.get("internships", [])) + len(recs.get("jobs", []))
    return {
        "student_id": profile.id,
        "skills_count": skills_count,
        "projects_count": projects_count,
        "total_applications": applications_count,
        "latest_assessment_score": 85,
        "matching_jobs_count": matching_count,
    }

@router.post("/apply/{opportunity_id}/{user_id}")
async def apply_to_opportunity(opportunity_id: int, user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not profile or not opp:
        raise HTTPException(status_code=404, detail="Profile or Opportunity not found")
    existing = db.query(Application).filter(Application.opportunity_id == opportunity_id, Application.student_id == profile.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this opportunity")
    new_app = Application(opportunity_id=opportunity_id, student_id=profile.id, status="Applied")
    db.add(new_app)
    db.commit()
    return {"message": "Application submitted successfully"}

@router.put("/profile/{user_id}")
async def update_profile(user_id: int, payload: dict, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    profile.phone = payload.get("phone", profile.phone)
    profile.location = payload.get("location", profile.location)
    profile.bio = payload.get("bio", profile.bio)
    profile.education = payload.get("education", profile.education)
    profile.institution = payload.get("institution", profile.institution)
    profile.cgpa = payload.get("cgpa", profile.cgpa)
    profile.linkedin = payload.get("linkedin", profile.linkedin)
    profile.profile_completed = True
    db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/skills/{user_id}")
async def add_skill(user_id: int, payload: dict, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    skill_name = payload.get("skill_name")
    proficiency = payload.get("proficiency", 50)
    if not skill_name:
        raise HTTPException(status_code=400, detail="Missing skill_name")
    existing = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id, StudentSkill.skill_name.ilike(skill_name)).first()
    if existing:
        existing.proficiency = proficiency
    else:
        new_skill = StudentSkill(student_id=profile.id, skill_name=skill_name, proficiency=proficiency)
        db.add(new_skill)
    db.commit()
    return {"message": "Skill processed successfully"}
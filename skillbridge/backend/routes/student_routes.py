# Student Routes
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import StudentProfile, StudentSkill, StudentProject
from models.opportunity import Opportunity, Application
from agents.recommendation_agent import RecommendationAgent
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    education: Optional[str] = None
    institution: Optional[str] = None
    linkedin_url: Optional[str] = None

class SkillEntry(BaseModel):
    skills: List[dict]
    projects: List[dict]

@router.get("/dashboard/{user_id}")
async def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).all()
    
    return {
        "skillScore": sum(s.proficiency for s in skills) / len(skills) if skills else 0,
        "matchingJobs": 5,
        "recommendedCourses": 3,
        "projects": 3
    }

@router.get("/profile/{user_id}")
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).all()
    
    return {
        "profile": {
            "full_name": profile.user.full_name if profile.user else "",
            "email": profile.user.email if profile.user else "",
            "education": profile.education,
            "institution": profile.institution,
            "linkedin_url": profile.linkedin_url
        },
        "skills": [{"skill_name": s.skill_name, "proficiency": s.proficiency} for s in skills]
    }

@router.put("/profile/{user_id}")
async def update_profile(user_id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    
    profile.profile_completed = True
    db.commit()
    
    return {"message": "Profile updated"}

@router.post("/skills/{user_id}")
async def add_skills(user_id: int, data: SkillEntry, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for skill in data.skills:
        student_skill = StudentSkill(
            student_id=profile.id,
            skill_name=skill["skill_name"],
            proficiency=skill.get("proficiency", 50)
        )
        db.add(student_skill)
    
    for project in data.projects:
        student_project = StudentProject(
            student_id=profile.id,
            project_name=project["project_name"],
            description=project.get("description", ""),
            technologies_used=project.get("technologies_used", [])
        )
        db.add(student_project)
    
    db.commit()
    return {"message": "Skills added"}

@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    skills = db.query(StudentSkill).filter(StudentSkill.student_id == profile.id).all()
    
    skill_report = {
        "skills": {s.skill_name: {"proficiency": s.proficiency} for s in skills}
    }
    
    student_profile = {
        "skills": [{"skill_name": s.skill_name, "proficiency": s.proficiency} for s in skills]
    }
    
    agent = RecommendationAgent()
    recommendations = agent.get_recommendations(student_profile, skill_report)
    
    return recommendations
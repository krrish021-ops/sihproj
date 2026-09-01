from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from models.student import StudentProfile, StudentSkill, StudentProject
from models.opportunity import Opportunity
from models.application import Application
from models.assessment import StudentAssessment
from models.course import Course
from services.matching_service import calculate_match_score

router = APIRouter(prefix="/student", tags=["Student"])

class ProfileUpdateRequest(BaseModel):
    college: Optional[str] = None
    department: Optional[str] = None
    year_of_study: Optional[int] = None
    cgpa: Optional[float] = None
    bio: Optional[str] = None
    resume_url: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None

class SkillAddRequest(BaseModel):
    skill_name: str
    self_rating: int = 5

class ProjectAddRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    tech_stack: Optional[str] = ""
    url: Optional[str] = ""

class ApplyRequest(BaseModel):
    cover_letter: Optional[str] = ""

def resolve_student_id(user_id: Optional[int], db: Session) -> int:
    if user_id:
        return user_id
    first_student = db.query(User).filter(User.role == "student").first()
    if first_student:
        return first_student.id
    raise HTTPException(status_code=400, detail="Student profile not found")

# SECTION 1: ALL INTERNSHIPS (Always visible)
@router.get("/internships")
@router.get("/opportunities")
@router.get("/all-internships")
def get_all_internships(db: Session = Depends(get_db)):
    opps = db.query(Opportunity).filter(Opportunity.status == "active").all()
    return [
        {
            "id": o.id, "title": o.title, "company_name": o.company_name,
            "location": o.location, "opportunity_type": o.opportunity_type,
            "stipend": o.stipend, "duration": o.duration,
            "required_skills": o.required_skills, "min_cgpa": o.min_cgpa,
            "description": o.description,
        }
        for o in opps
    ]

@router.get("/internships/{opp_id}")
@router.get("/opportunities/{opp_id}")
@router.get("/internships/{opp_id}/{user_id}")
def get_internship_detail(opp_id: int, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).filter(Opportunity.id == opp_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    target_id = resolve_student_id(user_id, db)
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == target_id).first()
    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all() if profile else []
    skill_lookup = {s.skill_name.lower().strip(): s for s in skills}

    req_list = [r.strip().lower() for r in (opp.required_skills or "").split(",") if r.strip()]
    missing = []
    matched = []
    for r in req_list:
        if r in skill_lookup:
            s = skill_lookup[r]
            matched.append({"skill": r.title(), "rating": s.verified_rating if s.is_verified else s.self_rating, "is_verified": bool(s.is_verified)})
        else:
            missing.append(r.title())

    gap_courses = []
    for m in missing:
        courses = db.query(Course).filter(Course.skill_tags.ilike(f"%{m}%")).all()
        if courses:
            gap_courses.append({"skill": m, "courses": [{"title": c.title, "provider": c.provider, "youtube_url": c.url, "duration": f"{int(c.duration_hours)}h", "is_free": True} for c in courses[:2]]})
        else:
            gap_courses.append({"skill": m, "courses": [{"title": f"Learn {m}", "provider": "YouTube", "youtube_url": f"https://www.youtube.com/results?search_query={m.replace(' ', '+')}+full+course", "duration": "4h", "is_free": True}]})

    match_score = calculate_match_score(target_id, opp_id, db)

    return {
        "id": opp.id, "title": opp.title, "company_name": opp.company_name,
        "location": opp.location, "opportunity_type": opp.opportunity_type,
        "stipend": opp.stipend, "duration": opp.duration,
        "required_skills": opp.required_skills, "min_cgpa": opp.min_cgpa,
        "description": opp.description, "match_score": match_score,
        "matched_skills": matched, "missing_skills": missing, "gap_courses": gap_courses,
    }

# SECTION 2: RECOMMENDATIONS (Only after assessment)
@router.get("/recommendations")
@router.get("/recommendations/{user_id}")
def get_recommendations_endpoint(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    from agents.recommendation_agent import get_recommendations
    target_id = resolve_student_id(user_id, db)
    return get_recommendations(target_id, db)

# SECTION 3: GAP COURSES (Based on assessment weaknesses)
@router.get("/gap-courses")
@router.get("/gap-courses/{user_id}")
@router.get("/bridge-courses")
@router.get("/bridge-courses/{user_id}")
def get_gap_courses_endpoint(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    from agents.recommendation_agent import get_recommendations
    target_id = resolve_student_id(user_id, db)
    data = get_recommendations(target_id, db)
    return {
        "gap_courses": data.get("gap_courses", []),
        "bridge_courses": data.get("bridge_courses", []),
        "skill_gaps": data.get("skill_gaps", []),
        "career_advice": data.get("career_advice", ""),
        "has_assessments": data.get("has_assessments", False),
        "message": data.get("message", "")
    }

# PROFILE & SKILLS
@router.get("/profile")
@router.get("/profile/{user_id}")
def get_profile(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    user = db.query(User).filter(User.id == target_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == target_id).first()
    if not profile:
        profile = StudentProfile(user_id=target_id, college="University", department="Computer Science")
        db.add(profile)
        db.commit()
        db.refresh(profile)

    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all()
    projects = db.query(StudentProject).filter(StudentProject.profile_id == profile.id).all()
    assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == target_id).all()

    return {
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role},
        "profile": {"id": profile.id, "college": profile.college, "department": profile.department, "year_of_study": profile.year_of_study, "cgpa": profile.cgpa, "bio": profile.bio, "resume_url": profile.resume_url, "github_url": profile.github_url, "linkedin_url": profile.linkedin_url},
        "skills": [{"id": s.id, "skill_name": s.skill_name, "self_rating": s.self_rating, "verified_rating": s.verified_rating, "is_verified": bool(s.is_verified)} for s in skills],
        "projects": [{"id": p.id, "title": p.title, "description": p.description, "tech_stack": p.tech_stack, "url": p.url} for p in projects],
        "assessments": [{"id": a.id, "skill_name": a.skill_name, "score": a.score, "verified_level": a.verified_level, "completed_at": str(a.completed_at)} for a in assessments]
    }

@router.put("/profile")
@router.put("/profile/{user_id}")
def update_profile(req: ProfileUpdateRequest, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == target_id).first()
    if not profile:
        profile = StudentProfile(user_id=target_id)
        db.add(profile)
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(profile, k, v)
    db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/skills")
@router.post("/skills/{user_id}")
def add_skill(req: SkillAddRequest, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == target_id).first()
    if not profile:
        profile = StudentProfile(user_id=target_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    existing = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id, StudentSkill.skill_name.ilike(req.skill_name)).first()
    if existing:
        existing.self_rating = req.self_rating
        db.commit()
        return {"message": f"Skill '{req.skill_name}' updated"}

    db.add(StudentSkill(profile_id=profile.id, skill_name=req.skill_name.strip(), self_rating=req.self_rating))
    db.commit()
    return {"message": f"Skill '{req.skill_name}' added"}

@router.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    sk = db.query(StudentSkill).filter(StudentSkill.id == skill_id).first()
    if sk:
        db.delete(sk)
        db.commit()
        return {"message": "Skill removed"}
    raise HTTPException(status_code=404, detail="Skill not found")

@router.post("/projects")
@router.post("/projects/{user_id}")
def add_project(req: ProjectAddRequest, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == target_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.add(StudentProject(profile_id=profile.id, title=req.title, description=req.description, tech_stack=req.tech_stack, url=req.url))
    db.commit()
    return {"message": "Project saved"}

@router.post("/apply/{opportunity_id}")
@router.post("/apply/{opportunity_id}/{user_id}")
def apply_opportunity(opportunity_id: int, req: ApplyRequest, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    if db.query(Application).filter(Application.opportunity_id == opportunity_id, Application.student_id == target_id).first():
        raise HTTPException(status_code=400, detail="Already applied")
    score = calculate_match_score(target_id, opportunity_id, db)
    app = Application(opportunity_id=opportunity_id, student_id=target_id, cover_letter=req.cover_letter, match_score=score)
    db.add(app)
    db.commit()
    return {"message": "Application submitted successfully", "match_score": score}

@router.get("/applications")
@router.get("/applications/{user_id}")
def my_applications(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    apps = db.query(Application).filter(Application.student_id == target_id).all()
    results = []
    for a in apps:
        opp = db.query(Opportunity).filter(Opportunity.id == a.opportunity_id).first()
        results.append({"id": a.id, "opportunity_id": a.opportunity_id, "opportunity_title": opp.title if opp else "Opportunity", "company_name": opp.company_name if opp else "Company", "status": a.status, "match_score": a.match_score, "applied_at": str(a.applied_at)})
    return results

@router.get("/dashboard")
@router.get("/dashboard/{user_id}")
def student_dashboard(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = resolve_student_id(user_id, db)
    user = db.query(User).filter(User.id == target_id).first()
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == target_id).first()
    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all() if profile else []
    apps = db.query(Application).filter(Application.student_id == target_id).all()
    assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == target_id).all()

    return {
        "user_name": user.name if user else "",
        "total_skills": len(skills),
        "verified_skills": sum(1 for s in skills if s.is_verified),
        "total_applications": len(apps),
        "pending_applications": sum(1 for a in apps if a.status == "applied"),
        "shortlisted": sum(1 for a in apps if a.status == "shortlisted"),
        "assessments_taken": len(assessments),
        "active_internships": db.query(Opportunity).filter(Opportunity.status == "active").count(),
    }

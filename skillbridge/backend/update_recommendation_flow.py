import os

files = {}

# 1. Updated Recommendation Agent (Assessment-gated)
files["agents/recommendation_agent.py"] = """import json
from sqlalchemy.orm import Session
from utils.llm_setup import execute_groq_prompt
from models.student import StudentProfile, StudentSkill, StudentProject
from models.opportunity import Opportunity
from models.course import Course
from models.assessment import StudentAssessment
from models.user import User

def get_recommendations(user_id: int, db: Session) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

    if not profile:
        profile = StudentProfile(user_id=user_id, college="University", department="Computer Science")
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # CRITICAL: Check if student has taken any assessments
    assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == user_id).all()
    has_assessments = len(assessments) > 0

    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all()
    projects = db.query(StudentProject).filter(StudentProject.profile_id == profile.id).all()

    # Build skill lookup
    skill_summary = []
    skill_lookup = {}
    for s in skills:
        if s.is_verified and s.verified_rating > 0:
            effective = s.verified_rating
        else:
            effective = s.self_rating * 0.6

        info = {
            "name": s.skill_name,
            "self_rating": s.self_rating,
            "verified_rating": s.verified_rating,
            "is_verified": bool(s.is_verified),
            "effective_rating": round(effective, 1)
        }
        skill_summary.append(info)
        skill_lookup[s.skill_name.lower().strip()] = info

    # If no assessments taken, return empty recommendations with prompt
    if not has_assessments:
        return {
            "career_advice": "",
            "recommended_internships": [],
            "matched_opportunities": [],
            "all_internships": [],
            "gap_courses": [],
            "bridge_courses": [],
            "skill_gaps": [],
            "skill_summary": skill_summary,
            "assessments_taken_count": 0,
            "has_assessments": False,
            "message": "Please complete at least one skill assessment to unlock personalized internship recommendations and gap courses."
        }

    # All active opportunities
    all_opps = db.query(Opportunity).filter(Opportunity.status == "active").all()
    recommended_internships = []

    for opp in all_opps:
        opp_data = {
            "id": opp.id,
            "title": opp.title,
            "company_name": opp.company_name,
            "location": opp.location,
            "opportunity_type": opp.opportunity_type,
            "stipend": opp.stipend,
            "duration": opp.duration,
            "required_skills": opp.required_skills,
            "min_cgpa": opp.min_cgpa,
            "description": opp.description,
        }

        req_list = [r.strip().lower() for r in (opp.required_skills or "").split(",") if r.strip()]
        if not req_list:
            continue

        matched_weight = 0.0
        missing_skills = []
        verified_count = 0

        for req in req_list:
            if req in skill_lookup:
                eff = skill_lookup[req]["effective_rating"]
                is_ver = skill_lookup[req]["is_verified"]
                if is_ver:
                    verified_count += 1
                    matched_weight += min((eff / 10.0) * 1.25, 1.0)
                else:
                    matched_weight += (eff / 10.0) * 0.75
            else:
                missing_skills.append(req.title())

        base_score = (matched_weight / len(req_list)) * 100.0

        if profile.cgpa and opp.min_cgpa and profile.cgpa >= opp.min_cgpa:
            base_score += 5.0

        base_score += min(len(assessments) * 2.0, 10.0)

        final_match_pct = round(min(max(base_score, 15.0), 100.0), 1)

        recommended_internships.append({
            **opp_data,
            "match_percentage": final_match_pct,
            "match_score": final_match_pct,
            "missing_skills": missing_skills,
            "verified_skills_matched": verified_count,
        })

    recommended_internships.sort(key=lambda x: x["match_percentage"], reverse=True)

    # Gap courses based on assessment results
    weak_skills_set = set()

    for m in recommended_internships[:6]:
        for ms in m.get("missing_skills", []):
            weak_skills_set.add(ms.strip())

    for s in skill_summary:
        if s["effective_rating"] < 6.0:
            weak_skills_set.add(s["name"].strip())

    for a in assessments:
        if a.score < 60:
            weak_skills_set.add(a.skill_name.strip())

    gap_courses = []
    for skill_name in list(weak_skills_set)[:8]:
        db_courses = db.query(Course).filter(Course.skill_tags.ilike(f"%{skill_name}%")).all()
        student_info = skill_lookup.get(skill_name.lower(), None)

        curated = []
        if db_courses:
            for c in db_courses[:3]:
                curated.append({
                    "id": c.id,
                    "title": c.title,
                    "provider": c.provider,
                    "url": c.url,
                    "youtube_url": c.url,
                    "duration": f"{int(c.duration_hours)} hours" if c.duration_hours else "Self-paced",
                    "difficulty": c.difficulty.title(),
                    "rating": c.rating or 4.8,
                    "is_free": bool(c.is_free)
                })
        else:
            curated.append({
                "id": 999,
                "title": f"Learn {skill_name.title()} - Full Course",
                "provider": "YouTube",
                "url": f"https://www.youtube.com/results?search_query={skill_name.replace(' ', '+')}+full+course",
                "youtube_url": f"https://www.youtube.com/results?search_query={skill_name.replace(' ', '+')}+full+course",
                "duration": "4-8 hours",
                "difficulty": "Beginner",
                "rating": 4.7,
                "is_free": True
            })

        gap_courses.append({
            "skill": skill_name.title(),
            "weak_skill": skill_name.title(),
            "current_rating": student_info["effective_rating"] if student_info else 0.0,
            "is_verified": student_info["is_verified"] if student_info else False,
            "courses": curated
        })

    # AI career advice
    skill_text = ", ".join([f"{s['name']} (Verified: {s['verified_rating']}/10)" if s['is_verified'] else f"{s['name']} (Self: {s['self_rating']}/10)" for s in skill_summary]) or "No skills"
    assessment_text = ", ".join([f"{a.skill_name}: {a.score}%" for a in assessments[:5]])

    ai_prompt = f"Career coaching for Indian student: {user.name if user else 'Candidate'}, Dept: {profile.department}, CGPA: {profile.cgpa}, Skills: {skill_text}, Assessment Results: {assessment_text}. Give 3 actionable bullet points on which skills to strengthen and which internships to target (include AYUSH sector if relevant)."
    career_advice = execute_groq_prompt(ai_prompt, model="llama-3.3-70b-versatile", temperature=0.3)
    if not career_advice.strip():
        career_advice = "Based on your assessment results, focus on strengthening your weakest verified skills and apply to internships where your match score exceeds 60%."

    return {
        "career_advice": career_advice,
        "recommended_internships": recommended_internships[:12],
        "matched_opportunities": recommended_internships[:12],
        "all_internships": [
            {
                "id": o.id, "title": o.title, "company_name": o.company_name, "location": o.location,
                "opportunity_type": o.opportunity_type, "stipend": o.stipend, "duration": o.duration,
                "required_skills": o.required_skills, "min_cgpa": o.min_cgpa, "description": o.description
            } for o in all_opps
        ],
        "gap_courses": gap_courses,
        "bridge_courses": gap_courses,
        "skill_gaps": [s for s in skill_summary if s["effective_rating"] < 6.0],
        "skill_summary": skill_summary,
        "assessments_taken_count": len(assessments),
        "has_assessments": True,
        "message": ""
    }
"""

# 2. Updated Student Routes
files["routes/student.py"] = """from fastapi import APIRouter, Depends, HTTPException
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
"""

for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Updated: {path}")

print("\n🚀 Backend recommendation flow updated.")

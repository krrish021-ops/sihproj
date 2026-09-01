from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.academician import Academician
from models.student import StudentProfile, StudentSkill, StudentProject
from models.application import Application
from models.opportunity import Opportunity
from models.assessment import StudentAssessment
from models.course import Course
from utils.auth import require_academician
from agents.academician_agent import get_predictive_analytics

router = APIRouter(prefix="/academician", tags=["Academician"])

@router.get("/dashboard")
def academician_dashboard(current_user: dict = Depends(require_academician), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    user = db.query(User).filter(User.id == user_id).first()
    acad = db.query(Academician).filter(Academician.user_id == user_id).first()

    dept = acad.department if acad else ""
    institution = acad.institution if acad else ""

    profiles = db.query(StudentProfile).filter(StudentProfile.department == dept).all() if dept else []
    if not profiles:
        profiles = db.query(StudentProfile).all()

    p_ids = [p.id for p in profiles]
    s_ids = [p.user_id for p in profiles]
    total_students = len(profiles)

    all_skills = db.query(StudentSkill).filter(StudentSkill.profile_id.in_(p_ids)).all() if p_ids else []
    skill_stats = {}
    for s in all_skills:
        n = s.skill_name
        if n not in skill_stats:
            skill_stats[n] = {"skill_name": n, "student_count": 0, "verified_count": 0, "total_rating": 0.0}
        skill_stats[n]["student_count"] += 1
        skill_stats[n]["total_rating"] += (s.verified_rating if s.is_verified else s.self_rating * 0.7)
        if s.is_verified:
            skill_stats[n]["verified_count"] += 1

    skill_distribution = []
    for n, d in sorted(skill_stats.items(), key=lambda x: x[1]["student_count"], reverse=True):
        avg = round(d["total_rating"] / d["student_count"], 1) if d["student_count"] else 0
        skill_distribution.append({"skill_name": n, "student_count": d["student_count"], "verified_count": d["verified_count"], "avg_proficiency": avg})

    apps = db.query(Application).filter(Application.student_id.in_(s_ids)).all() if s_ids else []
    funnel = {
        "total_students": total_students,
        "students_applied": len(set(a.student_id for a in apps)),
        "total_applications": len(apps),
        "applied": sum(1 for a in apps if a.status == "applied"),
        "shortlisted": sum(1 for a in apps if a.status == "shortlisted"),
        "interviewed": sum(1 for a in apps if a.status == "interviewed"),
        "offered": sum(1 for a in apps if a.status == "offered"),
        "accepted": sum(1 for a in apps if a.status == "accepted"),
        "rejected": sum(1 for a in apps if a.status == "rejected"),
    }
    placed = funnel["offered"] + funnel["accepted"]
    placement_rate = round((placed / total_students * 100), 1) if total_students else 0.0

    assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id.in_(s_ids)).all() if s_ids else []
    avg_assessment_score = round(sum(a.score for a in assessments) / len(assessments), 1) if assessments else 0.0

    active_opps = db.query(Opportunity).filter(Opportunity.status == "active").all()
    demand_skills = {}
    for o in active_opps:
        for sk in (o.required_skills or "").split(","):
            sk = sk.strip()
            if sk:
                demand_skills[sk] = demand_skills.get(sk, 0) + 1
    industry_demand = sorted([{"skill_name": k, "demand_count": v} for k, v in demand_skills.items()], key=lambda x: x["demand_count"], reverse=True)[:10]

    skill_gaps = []
    for d in industry_demand:
        s_data = skill_stats.get(d["skill_name"], None)
        if not s_data:
            skill_gaps.append({"skill_name": d["skill_name"], "industry_demand": d["demand_count"], "students_with_skill": 0, "avg_proficiency": 0.0, "gap_severity": "Critical", "recommended_action": f"Introduce {d['skill_name']} course immediately"})
        else:
            avg_p = round(s_data["total_rating"] / s_data["student_count"], 1) if s_data["student_count"] else 0
            if avg_p < 5.0 or s_data["verified_count"] < 2:
                severity = "Critical" if s_data["student_count"] == 0 else "Moderate"
                skill_gaps.append({"skill_name": d["skill_name"], "industry_demand": d["demand_count"], "students_with_skill": s_data["student_count"], "avg_proficiency": avg_p, "gap_severity": severity, "recommended_action": f"Strengthen {d['skill_name']} through verified assessments"})

    return {
        "user_name": user.name if user else "",
        "institution": institution,
        "department": dept or "All Departments",
        "total_students": total_students,
        "total_skills_tracked": len(skill_stats),
        "placement_rate": placement_rate,
        "total_placed": placed,
        "total_applications": len(apps),
        "assessments_completed": len(assessments),
        "avg_assessment_score": avg_assessment_score,
        "placement_funnel": funnel,
        "skill_distribution": skill_distribution[:15],
        "industry_demand": industry_demand,
        "skill_gaps": skill_gaps,
        "active_opportunities": len(active_opps),
        "available_courses": db.query(Course).count(),
    }

# NEW: Get all students with summary stats
@router.get("/students")
def get_all_students(current_user: dict = Depends(require_academician), db: Session = Depends(get_db)):
    acad = db.query(Academician).filter(Academician.user_id == current_user["user_id"]).first()
    dept = acad.department if acad else ""

    profiles = db.query(StudentProfile).filter(StudentProfile.department == dept).all() if dept else db.query(StudentProfile).all()
    if not profiles:
        profiles = db.query(StudentProfile).all()

    students = []
    for p in profiles:
        user = db.query(User).filter(User.id == p.user_id).first()
        if not user:
            continue

        skills = db.query(StudentSkill).filter(StudentSkill.profile_id == p.id).all()
        assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == p.user_id).all()
        apps = db.query(Application).filter(Application.student_id == p.user_id).all()
        projects = db.query(StudentProject).filter(StudentProject.profile_id == p.id).all()

        verified_count = sum(1 for s in skills if s.is_verified)
        avg_score = round(sum(a.score for a in assessments) / len(assessments), 1) if assessments else 0.0
        latest_status = apps[0].status if apps else "not_applied"

        students.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "college": p.college,
            "department": p.department,
            "year_of_study": p.year_of_study,
            "cgpa": p.cgpa,
            "total_skills": len(skills),
            "verified_skills": verified_count,
            "unverified_skills": len(skills) - verified_count,
            "assessments_taken": len(assessments),
            "avg_assessment_score": avg_score,
            "applications_sent": len(apps),
            "latest_application_status": latest_status,
            "projects_count": len(projects),
            "skill_names": [s.skill_name for s in skills],
        })

    students.sort(key=lambda x: x["avg_assessment_score"], reverse=True)
    return {"total": len(students), "students": students}

# NEW: Get detailed progress for a specific student
@router.get("/students/{student_id}")
def get_student_progress(student_id: int, current_user: dict = Depends(require_academician), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == student_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Student not found")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == student_id).first()
    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all() if profile else []
    assessments = db.query(StudentAssessment).filter(StudentAssessment.student_id == student_id).order_by(StudentAssessment.completed_at.desc()).all()
    apps = db.query(Application).filter(Application.student_id == student_id).all()
    projects = db.query(StudentProject).filter(StudentProject.profile_id == profile.id).all() if profile else []

    skill_details = []
    for s in skills:
        skill_assessments = [a for a in assessments if a.skill_name.lower() == s.skill_name.lower()]
        best_score = max([a.score for a in skill_assessments], default=0)
        attempts = len(skill_assessments)

        skill_details.append({
            "id": s.id,
            "skill_name": s.skill_name,
            "self_rating": s.self_rating,
            "verified_rating": s.verified_rating,
            "is_verified": bool(s.is_verified),
            "best_assessment_score": best_score,
            "assessment_attempts": attempts,
            "proficiency_gap": round(max(0, s.self_rating - s.verified_rating), 1) if s.is_verified else s.self_rating,
        })

    assessment_history = []
    for a in assessments:
        assessment_history.append({
            "id": a.id,
            "skill_name": a.skill_name,
            "score": a.score,
            "total_questions": a.total_questions,
            "correct_answers": a.correct_answers,
            "verified_level": a.verified_level,
            "time_taken_seconds": a.time_taken_seconds,
            "completed_at": str(a.completed_at),
        })

    application_details = []
    for app in apps:
        opp = db.query(Opportunity).filter(Opportunity.id == app.opportunity_id).first()
        application_details.append({
            "id": app.id,
            "opportunity_title": opp.title if opp else "Unknown",
            "company_name": opp.company_name if opp else "Unknown",
            "status": app.status,
            "match_score": app.match_score,
            "applied_at": str(app.applied_at),
        })

    project_details = []
    for proj in projects:
        project_details.append({
            "id": proj.id,
            "title": proj.title,
            "description": proj.description,
            "tech_stack": proj.tech_stack,
        })

    overall_progress = {
        "skill_verification_rate": round((sum(1 for s in skills if s.is_verified) / len(skills) * 100), 1) if skills else 0,
        "avg_assessment_score": round(sum(a.score for a in assessments) / len(assessments), 1) if assessments else 0,
        "application_conversion_rate": round((sum(1 for a in apps if a.status in ["shortlisted", "interviewed", "offered", "accepted"]) / len(apps) * 100), 1) if apps else 0,
        "placement_status": "Placed" if any(a.status in ["offered", "accepted"] for a in apps) else ("In Progress" if apps else "Not Started"),
    }

    return {
        "student": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
        "profile": {
            "college": profile.college if profile else "",
            "department": profile.department if profile else "",
            "year_of_study": profile.year_of_study if profile else 0,
            "cgpa": profile.cgpa if profile else 0,
            "bio": profile.bio if profile else "",
            "github_url": profile.github_url if profile else "",
            "linkedin_url": profile.linkedin_url if profile else "",
        },
        "skills": skill_details,
        "assessments": assessment_history,
        "applications": application_details,
        "projects": project_details,
        "overall_progress": overall_progress,
    }

@router.get("/predictive-analytics")
def predictive_analytics_endpoint(current_user: dict = Depends(require_academician), db: Session = Depends(get_db)):
    return get_predictive_analytics(current_user["user_id"], db)

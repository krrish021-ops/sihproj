"""
Academician Agent
"""
import json
from database import SessionLocal
from models.user import StudentProfile, StudentSkill, AcademicianProfile
from models.opportunity import Opportunity, OpportunityType
from services.matching_service import compute_match_detailed

def get_department_recommendations(user_id: int) -> dict:
    db = SessionLocal()
    try:
        acad = db.query(AcademicianProfile).filter(AcademicianProfile.user_id == user_id).first()
        institution = acad.institution if acad else "Institute of Technology"
        department = acad.department if acad else "Computer Science"
        students = db.query(StudentProfile).all()
        dept_skills = {}
        for student in students:
            skills = db.query(StudentSkill).filter(StudentSkill.student_id == student.id).all()
            for s in skills:
                name = s.skill_name.lower().strip()
                if name:
                    if name not in dept_skills:
                        dept_skills[name] = {"total": 0, "count": 0}
                    dept_skills[name]["total"] += s.proficiency
                    dept_skills[name]["count"] += 1
        avg_skills = [{"skill": name.title(), "proficiency": int(d["total"] / d["count"])} for name, d in dept_skills.items()]
        avg_skills.sort(key=lambda x: x["proficiency"], reverse=True)
        opps = db.query(Opportunity).filter(Opportunity.is_active == True, Opportunity.type == OpportunityType.INTERNSHIP).all()
        recommendations = []
        for o in opps:
            req = o.required_skills or []
            if isinstance(req, str):
                try:
                    req = json.loads(req)
                except Exception:
                    continue
            score, matched, missing = compute_match_detailed(avg_skills, req)
            if score >= 30:
                recommendations.append({
                    "id": o.id,
                    "title": o.title,
                    "company": o.recruiter.company_name if o.recruiter else "Partner Corp",
                    "location": o.location or "Remote",
                    "stipend": o.stipend or "Competitive",
                    "match_score": score,
                    "matched_skills": matched,
                    "missing_skills": missing,
                })
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        return {
            "institution": institution,
            "department": department,
            "student_count": len(students),
            "department_skills": avg_skills[:10],
            "skill_gaps": [s for s in avg_skills if s["proficiency"] < 60][:5],
            "recommended_internships": recommendations[:10],
        }
    finally:
        db.close()
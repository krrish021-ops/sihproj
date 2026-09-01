from sqlalchemy.orm import Session
from models.student import StudentProfile, StudentSkill
from models.opportunity import Opportunity

def calculate_match_score(student_id: int, opportunity_id: int, db: Session) -> float:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == student_id).first()
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not profile or not opp:
        return 50.0

    required = [s.strip().lower() for s in (opp.required_skills or "").split(",") if s.strip()]
    if not required:
        return 75.0

    skills = db.query(StudentSkill).filter(StudentSkill.profile_id == profile.id).all()
    skill_map = {s.skill_name.lower().strip(): s for s in skills}

    total_weight = 0.0
    for req in required:
        if req in skill_map:
            sk = skill_map[req]
            if sk.is_verified and sk.verified_rating > 0:
                total_weight += min(sk.verified_rating * 10.0 + 5.0, 100.0)
            else:
                total_weight += sk.self_rating * 7.5

    score = total_weight / len(required)
    if opp.min_cgpa and profile.cgpa and profile.cgpa >= opp.min_cgpa:
        score += 5.0

    return round(min(score, 100.0), 1)

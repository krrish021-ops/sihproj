import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal, Base
from models.user import User
from models.student import StudentProfile, StudentSkill, StudentProject
from models.recruiter import Recruiter
from models.academician import Academician
from models.opportunity import Opportunity
from models.course import Course
from utils.auth import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(User).first():
            print("Database already seeded.")
            return

        # 1. Course Catalog
        courses = [
            Course(title="Ayurveda Informatics & Digital Healthcare Records", provider="Ministry of AYUSH / Swayam", url="https://swayam.gov.in", skill_tags="Ayurveda Informatics, Healthcare, SQL", difficulty="beginner", duration_hours=40, is_free=1),
            Course(title="Deep Learning with PyTorch & Computer Vision", provider="NPTEL", url="https://nptel.ac.in", skill_tags="Machine Learning, Python, PyTorch, Computer Vision", difficulty="intermediate", duration_hours=60, is_free=1),
            Course(title="FastAPI High-Performance Microservices", provider="SkillBridge Academy", url="https://fastapi.tiangolo.com", skill_tags="FastAPI, Python, Docker, Backend", difficulty="intermediate", duration_hours=25, is_free=1),
            Course(title="Enterprise React & Next.js Architecture", provider="Coursera / Meta", url="https://coursera.org", skill_tags="React, JavaScript, Frontend", difficulty="intermediate", duration_hours=35, is_free=0),
        ]
        db.add_all(courses)
        db.commit()

        # 2. Students
        s1 = User(name="Rahul Sharma", email="rahul@student.com", password_hash=hash_password("password123"), role="student")
        db.add(s1)
        db.commit()
        db.refresh(s1)

        p1 = StudentProfile(user_id=s1.id, college="IIT Delhi", department="Computer Science", year_of_study=3, cgpa=8.8, bio="AI/ML developer passionate about national digital health systems.")
        db.add(p1)
        db.commit()
        db.refresh(p1)

        for sk, val, ver in [("Python", 8, 8.5), ("Machine Learning", 7, 7.8), ("FastAPI", 8, 8.0), ("Ayurveda Informatics", 6, 6.5)]:
            db.add(StudentSkill(profile_id=p1.id, skill_name=sk, self_rating=val, verified_rating=ver, is_verified=1))

        db.add(StudentProject(profile_id=p1.id, title="AyurVision: Herbal Specimen Classifier", description="Convolutional neural network for automatic identification of medicinal flora under AYUSH taxonomy.", tech_stack="Python, PyTorch, FastAPI, React"))

        # 3. Recruiter
        r1 = User(name="Amit Kumar", email="hr@techcorp.com", password_hash=hash_password("password123"), role="recruiter")
        db.add(r1)
        db.commit()
        db.refresh(r1)

        db.add(Recruiter(user_id=r1.id, company_name="National AYUSH Health-Tech Consortium", designation="Head of Engineering Recruitment"))

        db.add(Opportunity(
            recruiter_id=r1.id,
            title="Digital Health & AI Platform Engineer",
            description="Developing national-scale interoperable health data records conforming to Ministry of AYUSH benchmarks.",
            company_name="National AYUSH Health-Tech Consortium",
            location="New Delhi (Hybrid)",
            opportunity_type="internship",
            stipend=30000,
            duration="6 months",
            required_skills="Python, FastAPI, Machine Learning, Ayurveda Informatics",
            min_cgpa=7.5,
        ))

        db.add(Opportunity(
            recruiter_id=r1.id,
            title="Full-Stack Cloud Developer",
            description="Building cloud-native web portals for distributed student skill mapping.",
            company_name="TechCorp India",
            location="Bangalore",
            opportunity_type="placement",
            stipend=750000,
            duration="Full-Time",
            required_skills="React, JavaScript, Python, Docker",
            min_cgpa=7.0,
        ))

        # 4. Academician
        a1 = User(name="Prof. Anita Sharma", email="prof.sharma@college.edu", password_hash=hash_password("password123"), role="academician")
        db.add(a1)
        db.commit()
        db.refresh(a1)

        db.add(Academician(user_id=a1.id, institution="IIT Delhi", department="Computer Science", designation="Professor & Dean of Academics", specialization="Artificial Intelligence & Health Informatics"))

        db.commit()
        print("✅ Production database initialized and seeded successfully!")
        print("\nVerified Credentials:")
        print("  Student:     rahul@student.com / password123")
        print("  Recruiter:   hr@techcorp.com / password123")
        print("  Academician: prof.sharma@college.edu / password123")
    except Exception as e:
        db.rollback()
        print(f"Error initializing seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

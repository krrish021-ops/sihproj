import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import engine, SessionLocal, Base
from models.user import User
from models.recruiter import Recruiter
from models.opportunity import Opportunity
from models.course import Course
from utils.auth import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # Ensure recruiter exists
    ru = db.query(User).filter(User.role == "recruiter").first()
    if not ru:
        ru = User(name="Internshala Network", email="partner@internshala.com", password_hash=hash_password("password123"), role="recruiter")
        db.add(ru)
        db.commit()
        db.refresh(ru)
        db.add(Recruiter(user_id=ru.id, company_name="Internshala Hiring Network"))
        db.commit()
    rid = ru.id

    # Clear and reseed opportunities
    db.query(Opportunity).delete()
    opps = [
        Opportunity(recruiter_id=rid, title="Python Backend Developer Intern", company_name="TechCorp India", location="Bangalore (Remote)", opportunity_type="internship", stipend=18000, duration="3 months", required_skills="Python, Django, SQL, REST APIs", min_cgpa=6.5, description="Build scalable REST APIs using Python Django. Work with PostgreSQL and Redis caching."),
        Opportunity(recruiter_id=rid, title="Machine Learning Research Intern", company_name="AI Labs India", location="Hyderabad", opportunity_type="internship", stipend=25000, duration="6 months", required_skills="Python, Machine Learning, TensorFlow, Data Science", min_cgpa=7.5, description="Train NLP transformer models for clinical document analysis."),
        Opportunity(recruiter_id=rid, title="Full Stack React Developer", company_name="StartupHub", location="Mumbai (Remote)", opportunity_type="internship", stipend=22000, duration="6 months", required_skills="React, JavaScript, Node.js, MongoDB", min_cgpa=7.0, description="Build responsive web apps for ed-tech platform with 200K users."),
        Opportunity(recruiter_id=rid, title="AYUSH Digital Health Engineer", company_name="Ministry of AYUSH", location="New Delhi", opportunity_type="internship", stipend=20000, duration="4 months", required_skills="Python, React, SQL, FastAPI", min_cgpa=6.5, description="Build digital health records for AYUSH hospitals under National Digital Health Mission."),
        Opportunity(recruiter_id=rid, title="Data Analyst Intern", company_name="FinServe Analytics", location="Gurgaon (Remote)", opportunity_type="internship", stipend=16000, duration="3 months", required_skills="SQL, Python, Excel, Data Science", min_cgpa=6.5, description="Analyze financial data and build PowerBI dashboards."),
        Opportunity(recruiter_id=rid, title="DevOps & Cloud Intern", company_name="CloudFirst", location="Pune (Remote)", opportunity_type="internship", stipend=24000, duration="4 months", required_skills="Docker, AWS, Linux, Python", min_cgpa=7.0, description="Build CI/CD pipelines with GitHub Actions and AWS ECS."),
        Opportunity(recruiter_id=rid, title="Computer Vision AI Intern", company_name="AYUSH Wellness AI", location="Rishikesh", opportunity_type="internship", stipend=18000, duration="3 months", required_skills="Python, Computer Vision, Machine Learning", min_cgpa=6.5, description="Build yoga posture correction using MediaPipe and PyTorch."),
        Opportunity(recruiter_id=rid, title="Cybersecurity Intern", company_name="SecureNet India", location="Bangalore", opportunity_type="internship", stipend=22000, duration="6 months", required_skills="Cybersecurity, Linux, Python, Networking", min_cgpa=7.0, description="Penetration testing and vulnerability assessment."),
        Opportunity(recruiter_id=rid, title="React Frontend Developer", company_name="PixelCraft", location="Remote", opportunity_type="internship", stipend=15000, duration="3 months", required_skills="React, JavaScript, CSS, Redux", min_cgpa=6.0, description="Convert Figma designs to responsive React components."),
        Opportunity(recruiter_id=rid, title="FastAPI Microservices Intern", company_name="DataPipe", location="Chennai", opportunity_type="internship", stipend=20000, duration="5 months", required_skills="FastAPI, Python, SQL, Docker", min_cgpa=7.0, description="Design async REST APIs with Redis caching."),
        Opportunity(recruiter_id=rid, title="Java Spring Boot Intern", company_name="InfoSys", location="Hyderabad", opportunity_type="internship", stipend=18000, duration="6 months", required_skills="Java, Spring Boot, SQL, REST APIs", min_cgpa=7.0, description="Enterprise microservices for banking clients."),
        Opportunity(recruiter_id=rid, title="AYUSH Telemedicine Developer", company_name="Swasthya Digital", location="Delhi (Remote)", opportunity_type="internship", stipend=17000, duration="4 months", required_skills="React, Node.js, MongoDB", min_cgpa=6.5, description="Video consultation platform for rural AYUSH doctors."),
    ]
    db.add_all(opps)
    db.commit()
    print(f"Seeded {len(opps)} internships")

    # Clear and reseed YouTube courses
    db.query(Course).delete()
    courses = [
        Course(title="Python Full Course (6 Hours)", provider="Programming with Mosh", url="https://www.youtube.com/watch?v=_uQrJ0TkZlc", skill_tags="Python", difficulty="beginner", duration_hours=6, rating=4.9, is_free=1),
        Course(title="Python Advanced OOP", provider="Corey Schafer", url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM", skill_tags="Python", difficulty="advanced", duration_hours=8, rating=4.9, is_free=1),
        Course(title="React JS Full Course 2024", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=bMknfKXIFA8", skill_tags="React, JavaScript", difficulty="beginner", duration_hours=12, rating=4.8, is_free=1),
        Course(title="Redux Toolkit Tutorial", provider="Dave Gray", url="https://www.youtube.com/watch?v=NqzdVN2tyvQ", skill_tags="React, Redux, JavaScript", difficulty="intermediate", duration_hours=4, rating=4.7, is_free=1),
        Course(title="JavaScript Full Course", provider="SuperSimpleDev", url="https://www.youtube.com/watch?v=EerdGm-ehJQ", skill_tags="JavaScript", difficulty="beginner", duration_hours=22, rating=4.9, is_free=1),
        Course(title="Node.js Express Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=Oe421EPjeBE", skill_tags="Node.js, JavaScript", difficulty="intermediate", duration_hours=8, rating=4.8, is_free=1),
        Course(title="Machine Learning Full Course", provider="Simplilearn", url="https://www.youtube.com/watch?v=GwIo3gDZCVQ", skill_tags="Machine Learning, Python, Data Science", difficulty="intermediate", duration_hours=10, rating=4.7, is_free=1),
        Course(title="TensorFlow 2.0 Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=tPYj3fFJGjk", skill_tags="TensorFlow, Machine Learning", difficulty="intermediate", duration_hours=7, rating=4.7, is_free=1),
        Course(title="SQL Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=HXV3zeQKqGY", skill_tags="SQL", difficulty="beginner", duration_hours=4, rating=4.8, is_free=1),
        Course(title="Docker Full Course", provider="TechWorld with Nana", url="https://www.youtube.com/watch?v=3c-iBn73dDE", skill_tags="Docker", difficulty="intermediate", duration_hours=5, rating=4.9, is_free=1),
        Course(title="AWS Cloud Practitioner", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=3hLmDS179YE", skill_tags="AWS", difficulty="beginner", duration_hours=13, rating=4.8, is_free=1),
        Course(title="FastAPI Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=7t2alSnE2-I", skill_tags="FastAPI, Python", difficulty="intermediate", duration_hours=4, rating=4.7, is_free=1),
        Course(title="Django Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=F5mRW0jo-U4", skill_tags="Django, Python", difficulty="intermediate", duration_hours=16, rating=4.8, is_free=1),
        Course(title="Cybersecurity Full Course", provider="Simplilearn", url="https://www.youtube.com/watch?v=900x5hYGBPo", skill_tags="Cybersecurity", difficulty="beginner", duration_hours=11, rating=4.6, is_free=1),
        Course(title="Computer Vision OpenCV", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=oXlwWbU8l2o", skill_tags="Computer Vision, Python", difficulty="intermediate", duration_hours=9, rating=4.8, is_free=1),
        Course(title="MongoDB Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=ofme2o29ngU", skill_tags="MongoDB", difficulty="intermediate", duration_hours=6, rating=4.6, is_free=1),
        Course(title="Java Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=xk4_1vDrzzo", skill_tags="Java", difficulty="beginner", duration_hours=12, rating=4.7, is_free=1),
        Course(title="Linux Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=ROjZy1WbCIA", skill_tags="Linux", difficulty="beginner", duration_hours=9, rating=4.8, is_free=1),
        Course(title="Data Science Full Course", provider="Simplilearn", url="https://www.youtube.com/watch?v=-ETQ97mXXF0", skill_tags="Data Science, Python", difficulty="intermediate", duration_hours=14, rating=4.6, is_free=1),
        Course(title="CSS & Tailwind Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=UB1O30fR-EE", skill_tags="CSS", difficulty="beginner", duration_hours=5, rating=4.5, is_free=1),
        Course(title="REST API Design", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=lsMQRaeKNDk", skill_tags="REST APIs", difficulty="intermediate", duration_hours=3, rating=4.6, is_free=1),
        Course(title="Networking Fundamentals", provider="NetworkChuck", url="https://www.youtube.com/watch?v=qiQR5rTSshw", skill_tags="Networking", difficulty="beginner", duration_hours=6, rating=4.7, is_free=1),
    ]
    db.add_all(courses)
    db.commit()
    print(f"Seeded {len(courses)} YouTube courses")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()

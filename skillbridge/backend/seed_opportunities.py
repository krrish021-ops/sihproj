import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.user import User
from models.opportunity import Opportunity
from models.course import Course
from utils.auth import hash_password

def seed():
    db = SessionLocal()

    # Create a system recruiter if none exists
    recruiter = db.query(User).filter(User.role == "recruiter").first()
    if not recruiter:
        recruiter = User(
            name="System Recruiter",
            email="system@internshala.com",
            password_hash=hash_password("system123"),
            role="recruiter"
        )
        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)
        from models.recruiter import Recruiter
        db.add(Recruiter(user_id=recruiter.id, company_name="Internshala Partner Network"))
        db.commit()

    rid = recruiter.id

    # Only seed if no opportunities exist
    if db.query(Opportunity).count() > 0:
        print("Opportunities already exist. Skipping.")
    else:
        opportunities = [
            Opportunity(recruiter_id=rid, title="Python Developer Intern", company_name="TechCorp India", location="Bangalore (Remote)", opportunity_type="internship", stipend=15000, duration="3 months", required_skills="Python, Django, REST APIs, SQL", min_cgpa=7.0, description="Build scalable web applications using Python and Django. Exposure to microservices."),
            Opportunity(recruiter_id=rid, title="Machine Learning Research Intern", company_name="AI Labs India", location="Hyderabad", opportunity_type="internship", stipend=20000, duration="6 months", required_skills="Python, TensorFlow, Machine Learning, Data Science", min_cgpa=7.5, description="Research and develop ML models for healthcare including AYUSH medicine analysis."),
            Opportunity(recruiter_id=rid, title="Full Stack Developer Intern", company_name="StartupHub", location="Mumbai (Hybrid)", opportunity_type="internship", stipend=25000, duration="6 months", required_skills="React, Node.js, JavaScript, MongoDB", min_cgpa=7.0, description="Build end-to-end features for an ed-tech platform serving 100K+ users."),
            Opportunity(recruiter_id=rid, title="Data Analyst Intern", company_name="FinServe Analytics", location="Delhi (Remote)", opportunity_type="internship", stipend=12000, duration="3 months", required_skills="SQL, Python, Excel, Data Science", min_cgpa=6.5, description="Analyze financial data and create dashboards for business intelligence."),
            Opportunity(recruiter_id=rid, title="AYUSH Digital Health Developer", company_name="Ministry of AYUSH Partner", location="New Delhi", opportunity_type="internship", stipend=18000, duration="4 months", required_skills="Python, React, SQL, Ayurveda Informatics", min_cgpa=6.5, description="Develop digital health record systems for AYUSH practitioners under national digital health mission."),
            Opportunity(recruiter_id=rid, title="DevOps Engineer Intern", company_name="CloudFirst Technologies", location="Pune (Remote)", opportunity_type="internship", stipend=20000, duration="3 months", required_skills="Docker, AWS, Linux, Python", min_cgpa=7.0, description="Set up CI/CD pipelines and manage cloud infrastructure for SaaS products."),
            Opportunity(recruiter_id=rid, title="Cybersecurity Analyst Intern", company_name="SecureNet India", location="Bangalore", opportunity_type="internship", stipend=22000, duration="6 months", required_skills="Cybersecurity, Python, Linux, Networking", min_cgpa=7.0, description="Perform security audits and vulnerability assessments for enterprise clients."),
            Opportunity(recruiter_id=rid, title="Yoga & Wellness Tech Intern", company_name="AYUSH Wellness Corp", location="Rishikesh (Hybrid)", opportunity_type="internship", stipend=10000, duration="3 months", required_skills="Python, Computer Vision, Yoga Science", min_cgpa=6.0, description="Build AI-powered yoga posture correction system using computer vision."),
            Opportunity(recruiter_id=rid, title="React Frontend Developer", company_name="WebScale Solutions", location="Gurgaon (Remote)", opportunity_type="internship", stipend=18000, duration="4 months", required_skills="React, JavaScript, CSS, Redux", min_cgpa=6.5, description="Build responsive UI components for enterprise dashboards."),
            Opportunity(recruiter_id=rid, title="Backend Engineer - FastAPI", company_name="DataPipe Systems", location="Chennai", opportunity_type="internship", stipend=22000, duration="6 months", required_skills="Python, FastAPI, PostgreSQL, Docker", min_cgpa=7.5, description="Design and build high-performance REST APIs for data pipeline orchestration."),
            Opportunity(recruiter_id=rid, title="AI/NLP Engineer Intern", company_name="LangTech AI", location="Bangalore", opportunity_type="internship", stipend=25000, duration="6 months", required_skills="Python, Natural Language Processing, Machine Learning, TensorFlow", min_cgpa=8.0, description="Build LLM-powered chatbots and document analysis systems."),
            Opportunity(recruiter_id=rid, title="Java Developer Intern", company_name="InfoSys Digital", location="Hyderabad", opportunity_type="internship", stipend=16000, duration="3 months", required_skills="Java, Spring Boot, SQL, REST APIs", min_cgpa=7.0, description="Develop enterprise-grade microservices for banking clients."),
            Opportunity(recruiter_id=rid, title="Cloud Engineer Placement", company_name="AWS India", location="Mumbai", opportunity_type="placement", stipend=800000, duration="Full-time", required_skills="AWS, Docker, Python, Kubernetes", min_cgpa=7.5, description="Full-time cloud infrastructure role managing multi-region deployments."),
            Opportunity(recruiter_id=rid, title="AYUSH Telemedicine Platform Developer", company_name="Swasthya Digital", location="Delhi (Remote)", opportunity_type="internship", stipend=15000, duration="4 months", required_skills="React, Node.js, MongoDB, Ayurveda Informatics", min_cgpa=6.5, description="Build telemedicine platform connecting AYUSH doctors with rural patients."),
            Opportunity(recruiter_id=rid, title="Data Science Intern", company_name="AnalyticsPro", location="Bangalore (Hybrid)", opportunity_type="internship", stipend=20000, duration="4 months", required_skills="Python, Data Science, SQL, Machine Learning", min_cgpa=7.5, description="Work on customer churn prediction and recommendation engines."),
        ]
        db.add_all(opportunities)
        db.commit()
        print(f"Seeded {len(opportunities)} opportunities.")

    # Seed YouTube Course Catalog
    if db.query(Course).count() > 0:
        print("Courses already exist. Skipping.")
    else:
        courses = [
            Course(title="Python Full Course for Beginners", provider="Programming with Mosh", url="https://www.youtube.com/watch?v=_uQrJ0TkZlc", skill_tags="Python", difficulty="beginner", duration_hours=6, rating=4.9, is_free=1),
            Course(title="Python Advanced - OOP, Decorators, Generators", provider="Corey Schafer", url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM&list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc", skill_tags="Python", difficulty="advanced", duration_hours=8, rating=4.8, is_free=1),
            Course(title="React JS Full Course 2024", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=bMknfKXIFA8", skill_tags="React, JavaScript, Frontend", difficulty="beginner", duration_hours=12, rating=4.8, is_free=1),
            Course(title="React Advanced Patterns & Redux Toolkit", provider="PedroTech", url="https://www.youtube.com/watch?v=jCBVQAKUOxY", skill_tags="React, Redux, JavaScript", difficulty="advanced", duration_hours=6, rating=4.7, is_free=1),
            Course(title="JavaScript Full Course", provider="SuperSimpleDev", url="https://www.youtube.com/watch?v=EerdGm-ehJQ", skill_tags="JavaScript", difficulty="beginner", duration_hours=22, rating=4.9, is_free=1),
            Course(title="Node.js & Express Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=Oe421EPjeBE", skill_tags="Node.js, JavaScript, Backend", difficulty="intermediate", duration_hours=8, rating=4.7, is_free=1),
            Course(title="Machine Learning Full Course", provider="Simplilearn", url="https://www.youtube.com/watch?v=GwIo3gDZCVQ", skill_tags="Machine Learning, Python, Data Science", difficulty="intermediate", duration_hours=10, rating=4.6, is_free=1),
            Course(title="Deep Learning with TensorFlow 2.0", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=tPYj3fFJGjk", skill_tags="TensorFlow, Machine Learning, Python", difficulty="advanced", duration_hours=7, rating=4.7, is_free=1),
            Course(title="SQL Full Course for Beginners", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=HXV3zeQKqGY", skill_tags="SQL", difficulty="beginner", duration_hours=4, rating=4.8, is_free=1),
            Course(title="Docker Full Course", provider="TechWorld with Nana", url="https://www.youtube.com/watch?v=3c-iBn73dDE", skill_tags="Docker, DevOps", difficulty="intermediate", duration_hours=5, rating=4.8, is_free=1),
            Course(title="AWS Cloud Practitioner Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=3hLmDS179YE", skill_tags="AWS, Cloud", difficulty="beginner", duration_hours=13, rating=4.7, is_free=1),
            Course(title="FastAPI Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=7t2alSnE2-I", skill_tags="FastAPI, Python, Backend", difficulty="intermediate", duration_hours=4, rating=4.6, is_free=1),
            Course(title="Django Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=F5mRW0jo-U4", skill_tags="Django, Python, Backend", difficulty="intermediate", duration_hours=16, rating=4.7, is_free=1),
            Course(title="Cybersecurity Full Course", provider="Simplilearn", url="https://www.youtube.com/watch?v=900x5hYGBPo", skill_tags="Cybersecurity", difficulty="beginner", duration_hours=11, rating=4.5, is_free=1),
            Course(title="Natural Language Processing Full Course", provider="Stanford CS224N", url="https://www.youtube.com/watch?v=8rXD5-xhemo&list=PLoROMvodv4rOhcuXMZkNm7j3fVwBBY42z", skill_tags="Natural Language Processing, Machine Learning, Python", difficulty="advanced", duration_hours=20, rating=4.9, is_free=1),
            Course(title="Data Science Full Course", provider="Simplilearn", url="https://www.youtube.com/watch?v=-ETQ97mXXF0", skill_tags="Data Science, Python, SQL", difficulty="intermediate", duration_hours=14, rating=4.6, is_free=1),
            Course(title="Java Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=xk4_1vDrzzo", skill_tags="Java", difficulty="beginner", duration_hours=12, rating=4.7, is_free=1),
            Course(title="Kubernetes Full Course", provider="TechWorld with Nana", url="https://www.youtube.com/watch?v=X48VuDVv0do", skill_tags="Kubernetes, Docker, DevOps", difficulty="advanced", duration_hours=4, rating=4.8, is_free=1),
            Course(title="Linux Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=ROjZy1WbCIA", skill_tags="Linux", difficulty="beginner", duration_hours=9, rating=4.6, is_free=1),
            Course(title="MongoDB Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=ofme2o29ngU", skill_tags="MongoDB, Database", difficulty="intermediate", duration_hours=6, rating=4.5, is_free=1),
            Course(title="Ayurveda Basics - Digital Health", provider="AYUSH Ministry", url="https://www.youtube.com/watch?v=VbOBfMjGJpM", skill_tags="Ayurveda Informatics, Yoga Science", difficulty="beginner", duration_hours=3, rating=4.3, is_free=1),
            Course(title="Computer Vision with OpenCV", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=oXlwWbU8l2o", skill_tags="Computer Vision, Python, Machine Learning", difficulty="intermediate", duration_hours=9, rating=4.7, is_free=1),
            Course(title="Redux Toolkit Full Course", provider="Dave Gray", url="https://www.youtube.com/watch?v=NqzdVN2tyvQ", skill_tags="Redux, React, JavaScript", difficulty="intermediate", duration_hours=4, rating=4.6, is_free=1),
            Course(title="PostgreSQL Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=qw--VYLpxG4", skill_tags="PostgreSQL, SQL, Database", difficulty="intermediate", duration_hours=4, rating=4.7, is_free=1),
        ]
        db.add_all(courses)
        db.commit()
        print(f"Seeded {len(courses)} YouTube courses.")

    db.close()
    print("Done.")

if __name__ == "__main__":
    seed()

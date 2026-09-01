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
    # 1. Ensure Recruiter Exists
    recruiter_user = db.query(User).filter(User.role == "recruiter").first()
    if not recruiter_user:
        recruiter_user = User(
            name="Internshala Partner Network",
            email="partner@internshala.com",
            password_hash=hash_password("password123"),
            role="recruiter"
        )
        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)
        db.add(Recruiter(user_id=recruiter_user.id, company_name="Internshala Hiring Network", industry="Technology & Healthcare"))
        db.commit()

    rid = recruiter_user.id

    # 2. Seed All Internships
    existing_opps = db.query(Opportunity).count()
    if existing_opps < 5:
        db.query(Opportunity).delete()
        opportunities = [
            Opportunity(recruiter_id=rid, title="Python & Django Backend Intern", company_name="TechCorp India", location="Bangalore (Remote)", opportunity_type="internship", stipend=18000, duration="3 months", required_skills="Python, Django, REST APIs, SQL", min_cgpa=6.5, description="Build scalable web applications and REST APIs using Python and Django. Work with microservices architectures and database migrations."),
            Opportunity(recruiter_id=rid, title="Machine Learning & NLP Research Intern", company_name="AI Labs India", location="Hyderabad (Hybrid)", opportunity_type="internship", stipend=25000, duration="6 months", required_skills="Python, Machine Learning, TensorFlow, NLP, Data Science", min_cgpa=7.5, description="Research, train, and deploy NLP transformer models for Indian language document summarization and clinical notes analysis."),
            Opportunity(recruiter_id=rid, title="Full Stack React & Node Developer", company_name="StartupHub Technologies", location="Mumbai (Remote)", opportunity_type="internship", stipend=22000, duration="6 months", required_skills="React, Node.js, JavaScript, MongoDB, Redux", min_cgpa=7.0, description="Build end-to-end responsive web applications for ed-tech platforms serving over 200K active users."),
            Opportunity(recruiter_id=rid, title="AYUSH Digital Health Platform Engineer", company_name="Ministry of AYUSH Partner", location="New Delhi (Hybrid)", opportunity_type="internship", stipend=20000, duration="4 months", required_skills="Python, React, SQL, Ayurveda Informatics, FastAPI", min_cgpa=6.5, description="Develop FHIR-compliant digital health record systems and telemedicine interfaces for AYUSH hospitals under the National Digital Health Mission."),
            Opportunity(recruiter_id=rid, title="Data Analyst & BI Intern", company_name="FinServe Analytics", location="Gurgaon (Remote)", opportunity_type="internship", stipend=16000, duration="3 months", required_skills="SQL, Python, Excel, Data Science, PowerBI", min_cgpa=6.5, description="Analyze financial datasets, write complex SQL aggregations, and build interactive PowerBI business intelligence dashboards."),
            Opportunity(recruiter_id=rid, title="Cloud & DevOps Engineer Intern", company_name="CloudFirst Solutions", location="Pune (Remote)", opportunity_type="internship", stipend=24000, duration="4 months", required_skills="Docker, AWS, Linux, Python, Kubernetes", min_cgpa=7.0, description="Build and automate CI/CD deployment pipelines using GitHub Actions, Docker containers, and AWS ECS/EKS clusters."),
            Opportunity(recruiter_id=rid, title="Computer Vision & Yoga Posture AI Intern", company_name="AYUSH Wellness AI", location="Rishikesh (Hybrid)", opportunity_type="internship", stipend=18000, duration="3 months", required_skills="Python, Computer Vision, Machine Learning, OpenCV, Yoga Science", min_cgpa=6.5, description="Implement real-time pose estimation and posture correction feedback algorithms for yoga practitioners using MediaPipe and PyTorch."),
            Opportunity(recruiter_id=rid, title="Cybersecurity & Vulnerability Assessment Intern", company_name="SecureNet India", location="Bangalore", opportunity_type="internship", stipend=22000, duration="6 months", required_skills="Cybersecurity, Linux, Python, Networking, SQL", min_cgpa=7.0, description="Perform automated and manual penetration testing, vulnerability scanning, and security audits on cloud web applications."),
            Opportunity(recruiter_id=rid, title="Frontend React.js Developer", company_name="PixelCraft Studios", location="Remote", opportunity_type="internship", stipend=15000, duration="3 months", required_skills="React, JavaScript, CSS, HTML, Redux", min_cgpa=6.0, description="Translate Figma wireframes into pixel-perfect, responsive React components with animations and state management."),
            Opportunity(recruiter_id=rid, title="FastAPI High-Performance Microservices Intern", company_name="DataPipe Systems", location="Chennai", opportunity_type="internship", stipend=20000, duration="5 months", required_skills="FastAPI, Python, SQL, Docker, Redis", min_cgpa=7.0, description="Design async REST APIs with FastAPI, integrate Redis caching layers, and optimize database read/write throughput."),
            Opportunity(recruiter_id=rid, title="Java & Spring Boot Enterprise Intern", company_name="InfoSys Digital", location="Hyderabad", opportunity_type="internship", stipend=18000, duration="6 months", required_skills="Java, Spring Boot, SQL, REST APIs", min_cgpa=7.0, description="Develop microservices in Java Spring Boot with JPA/Hibernate for banking and enterprise supply chain clients."),
            Opportunity(recruiter_id=rid, title="AYUSH Telemedicine Mobile & Web Developer", company_name="Swasthya Digital", location="Delhi (Remote)", opportunity_type="internship", stipend=17000, duration="4 months", required_skills="React, JavaScript, Node.js, Ayurveda Informatics", min_cgpa=6.5, description="Build video consultation modules and appointment scheduling for rural AYUSH medical practitioners."),
        ]
        db.add_all(opportunities)
        db.commit()
        print(f"✅ Seeded {len(opportunities)} internships in database.")

    # 3. Seed YouTube Courses for Weak Skills & Gaps
    existing_courses = db.query(Course).count()
    if existing_courses < 5:
        db.query(Course).delete()
        courses = [
            Course(title="Python Full Course for Beginners (6 Hours)", provider="Programming with Mosh", url="https://www.youtube.com/watch?v=_uQrJ0TkZlc", skill_tags="Python, Backend", difficulty="beginner", duration_hours=6.0, rating=4.9, is_free=1),
            Course(title="Python Advanced OOP & Concurrency Masterclass", provider="Corey Schafer", url="https://www.youtube.com/watch?v=ZDa-Z5JzLYM", skill_tags="Python, Advanced Python", difficulty="advanced", duration_hours=8.0, rating=4.9, is_free=1),
            Course(title="React JS Complete Course 2024 (12 Hours)", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=bMknfKXIFA8", skill_tags="React, JavaScript, Frontend", difficulty="beginner", duration_hours=12.0, rating=4.8, is_free=1),
            Course(title="Redux Toolkit & State Management in React", provider="Dave Gray", url="https://www.youtube.com/watch?v=NqzdVN2tyvQ", skill_tags="React, Redux, JavaScript", difficulty="intermediate", duration_hours=4.0, rating=4.7, is_free=1),
            Course(title="JavaScript Complete Course (22 Hours)", provider="SuperSimpleDev", url="https://www.youtube.com/watch?v=EerdGm-ehJQ", skill_tags="JavaScript, Frontend", difficulty="beginner", duration_hours=22.0, rating=4.9, is_free=1),
            Course(title="Node.js & Express.js Full Backend Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=Oe421EPjeBE", skill_tags="Node.js, JavaScript, Backend", difficulty="intermediate", duration_hours=8.0, rating=4.8, is_free=1),
            Course(title="Machine Learning Full Course (10 Hours)", provider="Simplilearn", url="https://www.youtube.com/watch?v=GwIo3gDZCVQ", skill_tags="Machine Learning, Python, Data Science", difficulty="intermediate", duration_hours=10.0, rating=4.7, is_free=1),
            Course(title="Deep Learning with PyTorch & Neural Networks", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=GIsg-ZUy0MY", skill_tags="Machine Learning, PyTorch, Deep Learning", difficulty="advanced", duration_hours=9.0, rating=4.8, is_free=1),
            Course(title="TensorFlow 2.0 Full Deep Learning Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=tPYj3fFJGjk", skill_tags="TensorFlow, Machine Learning, Python", difficulty="intermediate", duration_hours=7.0, rating=4.7, is_free=1),
            Course(title="SQL Database Full Course for Beginners", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=HXV3zeQKqGY", skill_tags="SQL, Database", difficulty="beginner", duration_hours=4.5, rating=4.8, is_free=1),
            Course(title="PostgreSQL Advanced Queries & Index Optimization", provider="Amigoscode", url="https://www.youtube.com/watch?v=qw--VYLpxG4", skill_tags="SQL, PostgreSQL, Database", difficulty="advanced", duration_hours=4.0, rating=4.7, is_free=1),
            Course(title="Docker & Containerization Hands-on Tutorial", provider="TechWorld with Nana", url="https://www.youtube.com/watch?v=3c-iBn73dDE", skill_tags="Docker, DevOps", difficulty="intermediate", duration_hours=5.0, rating=4.9, is_free=1),
            Course(title="AWS Certified Cloud Practitioner Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=3hLmDS179YE", skill_tags="AWS, Cloud", difficulty="beginner", duration_hours=13.0, rating=4.8, is_free=1),
            Course(title="FastAPI Python Async Microservices Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=7t2alSnE2-I", skill_tags="FastAPI, Python, Backend", difficulty="intermediate", duration_hours=4.5, rating=4.7, is_free=1),
            Course(title="Django Web Development Full Course", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=F5mRW0jo-U4", skill_tags="Django, Python, Backend", difficulty="intermediate", duration_hours=16.0, rating=4.8, is_free=1),
            Course(title="Cybersecurity Fundamentals & Ethical Hacking", provider="Simplilearn", url="https://www.youtube.com/watch?v=900x5hYGBPo", skill_tags="Cybersecurity, Security", difficulty="beginner", duration_hours=11.0, rating=4.6, is_free=1),
            Course(title="Natural Language Processing (NLP) with Transformers", provider="Stanford University", url="https://www.youtube.com/watch?v=8rXD5-xhemo", skill_tags="NLP, Natural Language Processing, AI", difficulty="advanced", duration_hours=18.0, rating=4.9, is_free=1),
            Course(title="Computer Vision with OpenCV & Python", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=oXlwWbU8l2o", skill_tags="Computer Vision, OpenCV, Python", difficulty="intermediate", duration_hours=9.0, rating=4.8, is_free=1),
            Course(title="Ayurveda Informatics & Digital Health Introduction", provider="Ministry of AYUSH / Swayam", url="https://www.youtube.com/watch?v=VbOBfMjGJpM", skill_tags="Ayurveda Informatics, Yoga Science, Healthcare", difficulty="beginner", duration_hours=3.0, rating=4.5, is_free=1),
            Course(title="MongoDB NoSQL Database Tutorial", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=ofme2o29ngU", skill_tags="MongoDB, Database", difficulty="intermediate", duration_hours=6.0, rating=4.6, is_free=1),
            Course(title="Java Programming Full Course for Beginners", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=xk4_1vDrzzo", skill_tags="Java, Programming", difficulty="beginner", duration_hours=12.0, rating=4.7, is_free=1),
            Course(title="Linux Command Line & Shell Scripting", provider="FreeCodeCamp", url="https://www.youtube.com/watch?v=ROjZy1WbCIA", skill_tags="Linux, DevOps", difficulty="beginner", duration_hours=9.0, rating=4.8, is_free=1),
        ]
        db.add_all(courses)
        db.commit()
        print(f"✅ Seeded {len(courses)} YouTube courses in database.")

    print("🚀 Data seeding completed successfully.")
except Exception as e:
    db.rollback()
    print(f"❌ Error seeding: {e}")
finally:
    db.close()

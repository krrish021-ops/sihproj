# Seed Data
from database import Base, engine, SessionLocal
from models.user import User, StudentProfile, StudentSkill, StudentProject, RecruiterProfile, AcademicianProfile, UserRole
from models.opportunity import Opportunity, OpportunityType
from models.course import Course, Project
from datetime import datetime, timedelta
from passlib.context import CryptContext
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(User).count() > 0:
        print("Database already seeded!")
        db.close()
        return
    
    # Create Recruiter
    recruiter_user = User(
        email="hr@techcorp.com",
        password_hash=pwd_context.hash("TechCorp@123"),
        full_name="Rahul Sharma",
        role=UserRole.RECRUITER
    )
    db.add(recruiter_user)
    db.flush()
    
    recruiter_profile = RecruiterProfile(
        user_id=recruiter_user.id,
        company_name="TechCorp Solutions",
        company_website="https://techcorp.com",
        industry_type="Information Technology"
    )
    db.add(recruiter_profile)
    db.flush()
    
    # Create Academician
    academician_user = User(
        email="prof.sharma@college.edu",
        password_hash=pwd_context.hash("TechCorp@123"),
        full_name="Prof. Amit Sharma",
        role=UserRole.ACADEMICIAN
    )
    db.add(academician_user)
    db.flush()
    
    academician_profile = AcademicianProfile(
        user_id=academician_user.id,
        institution="IIT Delhi",
        department="Computer Science"
    )
    db.add(academician_profile)
    
    # Create Courses
    courses = [
        Course(
            title="Python for Data Science and Machine Learning",
            provider="Udemy",
            instructor="Jose Portilla",
            rating=4.7,
            enrollment_count=450000,
            duration_hours=25,
            level="Beginner",
            skills_covered=["Python", "Data Science", "Machine Learning"],
            price=499,
            original_price=3499,
            course_url="https://www.udemy.com/course/python-for-data-science/"
        ),
        Course(
            title="The Complete JavaScript Course 2024",
            provider="Udemy",
            instructor="Jonas Schmedtmann",
            rating=4.8,
            enrollment_count=800000,
            duration_hours=69,
            level="Beginner",
            skills_covered=["JavaScript", "HTML", "CSS"],
            price=529,
            original_price=3699,
            course_url="https://www.udemy.com/course/the-complete-javascript-course/"
        ),
        Course(
            title="React - The Complete Guide 2024",
            provider="Udemy",
            instructor="Maximilian Schwarzmüller",
            rating=4.7,
            enrollment_count=650000,
            duration_hours=48,
            level="Intermediate",
            skills_covered=["React", "Redux", "JavaScript"],
            price=549,
            original_price=3799,
            course_url="https://www.udemy.com/course/react-the-complete-guide/"
        ),
        Course(
            title="Machine Learning A-Z",
            provider="Udemy",
            instructor="Kirill Eremenko",
            rating=4.5,
            enrollment_count=700000,
            duration_hours=42,
            level="Intermediate",
            skills_covered=["Machine Learning", "Python"],
            price=549,
            original_price=3799,
            course_url="https://www.udemy.com/course/machinelearning/"
        ),
        Course(
            title="SQL for Data Analysis",
            provider="Coursera",
            instructor="Duke University",
            rating=4.6,
            enrollment_count=120000,
            duration_hours=20,
            level="Intermediate",
            skills_covered=["SQL", "Data Analysis"],
            price=399,
            original_price=2999,
            course_url="https://www.coursera.org/learn/sql-for-data-analysis"
        ),
        Course(
            title="Full Stack Web Development Bootcamp",
            provider="Udemy",
            instructor="Angela Yu",
            rating=4.8,
            enrollment_count=900000,
            duration_hours=62,
            level="Beginner",
            skills_covered=["HTML", "CSS", "JavaScript", "Node.js", "React"],
            price=529,
            original_price=3699,
            course_url="https://www.udemy.com/course/the-complete-web-development-bootcamp/"
        ),
    ]
    
    for course in courses:
        db.add(course)
    
    # Create Projects
    projects = [
        Project(
            title="Build a Todo List Application",
            description="Create a full-featured todo list app with React",
            skills_taught=["React", "JavaScript", "HTML", "CSS"],
            difficulty="Beginner",
            estimated_hours=10,
            learning_outcome="Understand React components and state management"
        ),
        Project(
            title="E-commerce Website",
            description="Build a complete e-commerce platform",
            skills_taught=["React", "Node.js", "MongoDB"],
            difficulty="Intermediate",
            estimated_hours=40,
            learning_outcome="Full-stack development"
        ),
        Project(
            title="Portfolio Website",
            description="Create a stunning portfolio website",
            skills_taught=["HTML", "CSS", "JavaScript"],
            difficulty="Beginner",
            estimated_hours=15,
            learning_outcome="Responsive design"
        ),
        Project(
            title="Chat Application",
            description="Build a real-time chat application",
            skills_taught=["Node.js", "Socket.io", "React"],
            difficulty="Intermediate",
            estimated_hours=25,
            learning_outcome="WebSocket communication"
        ),
        Project(
            title="Data Analysis Dashboard",
            description="Create a data visualization dashboard",
            skills_taught=["Python", "Pandas", "Plotly"],
            difficulty="Intermediate",
            estimated_hours=20,
            learning_outcome="Data analysis and visualization"
        ),
    ]
    
    for project in projects:
        db.add(project)
    
    # Create Opportunities
    opportunities = [
        Opportunity(
            recruiter_id=recruiter_profile.id,
            title="Frontend Developer Intern",
            description="Looking for passionate frontend developers",
            type=OpportunityType.INTERNSHIP,
            required_skills=[
                {"skill": "JavaScript", "proficiency": 70},
                {"skill": "React", "proficiency": 60},
                {"skill": "HTML", "proficiency": 80},
                {"skill": "CSS", "proficiency": 70}
            ],
            location="Bangalore",
            stipend="₹25,000/month",
            duration="3 months",
            is_active=True
        ),
        Opportunity(
            recruiter_id=recruiter_profile.id,
            title="Python Developer - Full Time",
            description="Join our backend team",
            type=OpportunityType.JOB,
            required_skills=[
                {"skill": "Python", "proficiency": 80},
                {"skill": "Django", "proficiency": 60},
                {"skill": "PostgreSQL", "proficiency": 50}
            ],
            location="Remote",
            stipend="₹8,00,000/year",
            duration="Full-time",
            is_active=True
        ),
        Opportunity(
            recruiter_id=recruiter_profile.id,
            title="Mobile App Development Project",
            description="Develop a cross-platform mobile app",
            type=OpportunityType.PROJECT,
            required_skills=[
                {"skill": "React Native", "proficiency": 70},
                {"skill": "JavaScript", "proficiency": 75}
            ],
            location="Remote",
            stipend="₹50,000/project",
            duration="2 months",
            is_active=True
        ),
        Opportunity(
            recruiter_id=recruiter_profile.id,
            title="Data Analyst Intern",
            description="Work with large datasets",
            type=OpportunityType.INTERNSHIP,
            required_skills=[
                {"skill": "Python", "proficiency": 60},
                {"skill": "SQL", "proficiency": 70},
                {"skill": "Data Analysis", "proficiency": 50}
            ],
            location="Mumbai",
            stipend="₹20,000/month",
            duration="6 months",
            is_active=True
        ),
    ]
    
    for opportunity in opportunities:
        db.add(opportunity)
    
    db.commit()
    db.close()
    print("✅ Database seeded successfully!")
    print("Test Accounts:")
    print("Recruiter: hr@techcorp.com / TechCorp@123")
    print("Academician: prof.sharma@college.edu / TechCorp@123")

if __name__ == "__main__":
    seed_database()
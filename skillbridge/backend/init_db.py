import os
from database import engine, Base
from models.user import User
from models.student import StudentProfile, StudentSkill, StudentProject
from models.recruiter import Recruiter
from models.academician import Academician
from models.opportunity import Opportunity
from models.application import Application
from models.assessment import Assessment, Question, StudentAssessment
from models.course import Course
from models.project import Project

def init_clean_database():
    print("🔄 Creating fresh database schema with zero demo users...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Clean production SQLite database initialized successfully!")
    print("📁 Storage file: skillbridge.db")
    print("🚀 Ready for real signups and live data persistence.")

if __name__ == "__main__":
    init_clean_database()

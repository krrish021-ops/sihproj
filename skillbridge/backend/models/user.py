# User Model
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"
    ACADEMICIAN = "academician"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    role = Column(Enum(UserRole))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    recruiter_profile = relationship("RecruiterProfile", back_populates="user", uselist=False)
    academician_profile = relationship("AcademicianProfile", back_populates="user", uselist=False)

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    education = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    cgpa = Column(Float, nullable=True)
    linkedin_url = Column(String, nullable=True)
    profile_completed = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="student_profile")
    skills = relationship("StudentSkill", back_populates="student")
    projects = relationship("StudentProject", back_populates="student")
    applications = relationship("Application", back_populates="student")
    assessments = relationship("StudentAssessment", back_populates="student")

class StudentSkill(Base):
    __tablename__ = "student_skills"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    skill_name = Column(String)
    skill_category = Column(String, default="technical")
    proficiency = Column(Float, default=50)
    is_verified = Column(Boolean, default=False)
    
    student = relationship("StudentProfile", back_populates="skills")

class StudentProject(Base):
    __tablename__ = "student_projects"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    project_name = Column(String)
    description = Column(Text, nullable=True)
    technologies_used = Column(JSON, default=list)
    
    student = relationship("StudentProfile", back_populates="projects")

class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String, nullable=True)
    company_website = Column(String, nullable=True)
    industry_type = Column(String, nullable=True)
    
    user = relationship("User", back_populates="recruiter_profile")
    opportunities = relationship("Opportunity", back_populates="recruiter")

class AcademicianProfile(Base):
    __tablename__ = "academician_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    institution = Column(String, nullable=True)
    department = Column(String, nullable=True)
    
    user = relationship("User", back_populates="academician_profile")
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    college = Column(String, default="")
    department = Column(String, default="")
    year_of_study = Column(Integer, default=1)
    cgpa = Column(Float, default=0.0)
    bio = Column(Text, default="")
    resume_url = Column(String, default="")
    github_url = Column(String, default="")
    linkedin_url = Column(String, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    skills = relationship("StudentSkill", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("StudentProject", back_populates="profile", cascade="all, delete-orphan")

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String, nullable=False)
    self_rating = Column(Integer, default=5)
    verified_rating = Column(Float, default=0.0)
    is_verified = Column(Integer, default=0)

    profile = relationship("StudentProfile", back_populates="skills")

class StudentProject(Base):
    __tablename__ = "student_projects"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    tech_stack = Column(String, default="")
    url = Column(String, default="")

    profile = relationship("StudentProfile", back_populates="projects")

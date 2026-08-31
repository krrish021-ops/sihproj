# Opportunity Model
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class OpportunityType(str, enum.Enum):
    INTERNSHIP = "internship"
    JOB = "job"
    PROJECT = "project"

class Opportunity(Base):
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True)
    recruiter_id = Column(Integer, ForeignKey("recruiter_profiles.id"))
    title = Column(String)
    description = Column(Text)
    type = Column(Enum(OpportunityType))
    required_skills = Column(JSON)
    location = Column(String, nullable=True)
    stipend = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_applications = Column(Integer, default=0)
    shortlisted_count = Column(Integer, default=0)
    rejected_count = Column(Integer, default=0)
    
    recruiter = relationship("RecruiterProfile", back_populates="opportunities")
    applications = relationship("Application", back_populates="opportunity")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    status = Column(String, default="applied")
    cover_letter = Column(Text, default="")
    match_score = Column(Float, default=0)
    applied_at = Column(DateTime, default=datetime.utcnow)
    
    opportunity = relationship("Opportunity", back_populates="applications")
    student = relationship("StudentProfile", back_populates="applications")
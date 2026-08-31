# Assessment Model
from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    question_text = Column(Text)
    skill_name = Column(String)
    difficulty = Column(String)
    options = Column(JSON)
    correct_answer = Column(String)
    explanation = Column(Text, nullable=True)

class StudentAssessment(Base):
    __tablename__ = "student_assessments"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    score = Column(Float)
    skill_scores = Column(JSON)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("StudentProfile", back_populates="assessments")
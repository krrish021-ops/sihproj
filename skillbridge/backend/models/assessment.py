from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    skill_name = Column(String, nullable=False)
    difficulty = Column(String, default="intermediate")
    total_questions = Column(Integer, default=5)
    time_limit_minutes = Column(Integer, default=20)
    created_at = Column(DateTime, server_default=func.now())

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=True)
    skill_name = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    difficulty = Column(String, default="intermediate")
    explanation = Column(Text, default="")
    scenario = Column(Text, default="")

class StudentAssessment(Base):
    __tablename__ = "student_assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="SET NULL"), nullable=True)
    skill_name = Column(String, nullable=False)
    score = Column(Float, default=0.0)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    time_taken_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime, server_default=func.now())
    verified_level = Column(String, default="beginner")

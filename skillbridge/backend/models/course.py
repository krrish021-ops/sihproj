# Course Model
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from database import Base
from datetime import datetime

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    provider = Column(String)
    instructor = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    rating = Column(Float, default=4.5)
    enrollment_count = Column(Integer, default=0)
    duration_hours = Column(Float, default=10)
    level = Column(String, default="Beginner")
    skills_covered = Column(JSON)
    price = Column(Float, default=499)
    original_price = Column(Float, default=1999)
    course_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    skills_taught = Column(JSON)
    difficulty = Column(String, default="Beginner")
    estimated_hours = Column(Integer, default=10)
    learning_outcome = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
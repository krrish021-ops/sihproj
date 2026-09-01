from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    provider = Column(String, default="")
    url = Column(String, default="")
    skill_tags = Column(String, default="")
    difficulty = Column(String, default="beginner")
    duration_hours = Column(Float, default=0.0)
    rating = Column(Float, default=4.5)
    description = Column(Text, default="")
    is_free = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())

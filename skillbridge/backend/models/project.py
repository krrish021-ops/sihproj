from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Project(Base):
    __tablename__ = "projects_catalog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    difficulty = Column(String, default="beginner")
    skill_tags = Column(String, default="")
    estimated_hours = Column(Integer, default=10)
    category = Column(String, default="")
    created_at = Column(DateTime, server_default=func.now())

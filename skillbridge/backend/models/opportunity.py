from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.sql import func
from database import Base

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    company_name = Column(String, default="")
    location = Column(String, default="")
    opportunity_type = Column(String, default="internship")
    stipend = Column(Float, default=0.0)
    duration = Column(String, default="")
    required_skills = Column(Text, default="")
    min_cgpa = Column(Float, default=0.0)
    application_deadline = Column(String, default="")
    status = Column(String, default="active")
    max_applicants = Column(Integer, default=100)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

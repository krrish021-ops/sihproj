from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    company_name = Column(String, nullable=False)
    company_website = Column(String, default="")
    designation = Column(String, default="")
    industry = Column(String, default="")
    company_size = Column(String, default="")
    description = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())

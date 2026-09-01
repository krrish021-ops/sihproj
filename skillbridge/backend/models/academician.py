from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Academician(Base):
    __tablename__ = "academicians"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    institution = Column(String, nullable=False)
    department = Column(String, default="")
    designation = Column(String, default="")
    specialization = Column(String, default="")
    experience_years = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

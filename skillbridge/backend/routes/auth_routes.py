"""
Authentication Routes
=====================
Handles user registration and login for Students, Recruiters, and Academicians.
Supports multiple endpoint aliases (/register, /signup, /login, /signin).
"""

import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from database import get_db
from models.user import User, UserRole, StudentProfile, RecruiterProfile, AcademicianProfile

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "skillbridge_super_secret_jwt_key_2025")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

router = APIRouter(prefix="", tags=["auth"])


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
@router.post("/signup")
@router.post("/api/auth/register")
@router.post("/api/auth/signup")
@router.post("/auth/register")
@router.post("/auth/signup")
async def register(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()
    full_name = payload.get("full_name") or payload.get("name") or "New User"
    role_str = payload.get("role", "student").strip().lower()

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    if role_str == "recruiter":
        role_enum = UserRole.RECRUITER
    elif role_str == "academician":
        role_enum = UserRole.ACADEMICIAN
    else:
        role_enum = UserRole.STUDENT

    new_user = User(
        email=email,
        password_hash=pwd_context.hash(password),
        full_name=full_name,
        role=role_enum
    )
    db.add(new_user)
    db.flush()

    if role_enum == UserRole.STUDENT:
        profile = StudentProfile(
            user_id=new_user.id,
            education=payload.get("education", "Undergraduate"),
            institution=payload.get("institution", "Partner University"),
            profile_completed=True
        )
        db.add(profile)
    elif role_enum == UserRole.RECRUITER:
        profile = RecruiterProfile(
            user_id=new_user.id,
            company_name=payload.get("company_name") or payload.get("company") or f"{full_name} Corp",
            industry_type="Tech"
        )
        db.add(profile)
    elif role_enum == UserRole.ACADEMICIAN:
        profile = AcademicianProfile(
            user_id=new_user.id,
            institution=payload.get("institution", "Engineering College"),
            department=payload.get("department", "Computer Science")
        )
        db.add(profile)

    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "id": new_user.id, "role": role_str})

    return {
        "message": "User registered successfully",
        "access_token": token,
        "token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": role_str
        }
    }


@router.post("/login")
@router.post("/signin")
@router.post("/api/auth/login")
@router.post("/api/auth/signin")
@router.post("/auth/login")
@router.post("/auth/signin")
async def login(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    role_val = user.role.value if hasattr(user.role, "value") else str(user.role).lower()
    token = create_access_token({"sub": user.email, "id": user.id, "role": role_val})

    return {
        "message": "Login successful",
        "access_token": token,
        "token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role_val
        }
    }
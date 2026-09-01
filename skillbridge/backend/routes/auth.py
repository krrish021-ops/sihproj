from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from models.student import StudentProfile
from models.recruiter import Recruiter
from models.academician import Academician
from utils.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(tags=["Authentication"])

class SignupRequest(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = "student"
    user_type: Optional[str] = None
    college: Optional[str] = ""
    department: Optional[str] = ""
    company_name: Optional[str] = ""
    institution: Optional[str] = ""

    def get_name(self) -> str:
        return self.name or self.full_name or self.email.split("@")[0]

    def get_role(self) -> str:
        r = (self.role or self.user_type or "student").lower()
        if r in ["student", "recruiter", "academician"]:
            return r
        if "recruiter" in r or "company" in r or "hr" in r:
            return "recruiter"
        if "acad" in r or "prof" in r or "faculty" in r:
            return "academician"
        return "student"

class LoginRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    userEmail: Optional[str] = None
    password: str

    def get_email(self) -> str:
        return (self.email or self.username or self.userEmail or "").strip().lower()

@router.post("/auth/signup")
@router.post("/auth/register")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    email = req.email.strip().lower()
    name = req.get_name()
    role = req.get_role()

    print(f"📝 [SIGNUP ATTEMPT] Name: '{name}', Email: '{email}', Role: '{role}'")

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"❌ [SIGNUP FAILED] Email '{email}' is already registered.")
        raise HTTPException(status_code=400, detail="Email already registered in the system")

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(req.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if role == "student":
        db.add(StudentProfile(user_id=user.id, college=req.college or "University", department=req.department or "Computer Science"))
    elif role == "recruiter":
        db.add(Recruiter(user_id=user.id, company_name=req.company_name or "Enterprise Partner"))
    elif role == "academician":
        db.add(Academician(user_id=user.id, institution=req.institution or "Academic Institute", department=req.department or "Engineering"))
    db.commit()

    print(f"✅ [SIGNUP SUCCESS] User ID {user.id} ({user.email}) registered as {role}.")

    token = create_access_token(data={"user_id": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    }

@router.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    email = req.get_email()
    print(f"🔑 [LOGIN ATTEMPT] Received login request for email: '{email}'")

    if not email:
        print("❌ [LOGIN FAILED] No email or username provided in request.")
        raise HTTPException(status_code=400, detail="Email or username is required")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"❌ [LOGIN FAILED] No user found with email '{email}'. Please register first.")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(req.password, user.password_hash):
        print(f"❌ [LOGIN FAILED] Incorrect password for user '{email}'.")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    print(f"✅ [LOGIN SUCCESS] User '{user.name}' ({user.email}) logged in successfully as {user.role}.")
    token = create_access_token(data={"user_id": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    }

@router.get("/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

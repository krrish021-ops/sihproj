import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.auth import router as auth_router
from routes.student import router as student_router
from routes.recruiter import router as recruiter_router
from routes.assessment import router as assessment_router
from routes.academician import router as academician_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SkillBridge API",
    description="AI-Powered Skill Mapping, Internship & Placement Portal — Ministry of AYUSH",
    version="2.1.0"
)

# Middleware to automatically fix double /api/api prefixes from frontend/Vite proxy
@app.middleware("http")
async def fix_duplicate_api_prefix(request: Request, call_next):
    if request.scope["path"].startswith("/api/api/"):
        request.scope["path"] = request.scope["path"].replace("/api/api/", "/api/", 1)
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers with both /api prefix and root prefix
app.include_router(auth_router, prefix="/api")
app.include_router(auth_router)

app.include_router(student_router, prefix="/api")
app.include_router(student_router)

app.include_router(recruiter_router, prefix="/api")
app.include_router(recruiter_router)

app.include_router(assessment_router, prefix="/api")
app.include_router(assessment_router)

app.include_router(academician_router, prefix="/api")
app.include_router(academician_router)

@app.get("/")
@app.get("/api")
def root():
    return {
        "name": "SkillBridge API",
        "status": "online",
        "sponsor": "Ministry of AYUSH",
        "docs": "/docs"
    }

@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

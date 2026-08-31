"""
SkillBridge FastAPI Server Gateway
==================================
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import router as auth_router
from routes.student_routes import router as student_router
from routes.recruiter_routes import router as recruiter_router
from routes.assessment_routes import router as assessment_router
from routes.academician_routes import router as academician_router

app = FastAPI(title="SkillBridge API Gateway", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Router (mounted globally and on /api/auth)
app.include_router(auth_router)
app.include_router(auth_router, prefix="/api/auth")
app.include_router(auth_router, prefix="/auth")

# Feature Routers
app.include_router(student_router)
app.include_router(recruiter_router)
app.include_router(assessment_router)
app.include_router(academician_router)

@app.get("/")
async def root():
    return {"status": "online", "service": "skillbridge-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
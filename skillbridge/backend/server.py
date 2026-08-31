from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth_routes, student_routes, recruiter_routes, assessment_routes
from utils.langsmith_config import get_langsmith_status
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillBridge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(student_routes.router, prefix="/api/student", tags=["Student"])
app.include_router(recruiter_routes.router, prefix="/api/recruiter", tags=["Recruiter"])
app.include_router(assessment_routes.router, prefix="/api/assessment", tags=["Assessment"])

@app.get("/")
async def root():
    return {"message": "SkillBridge API is running"}

@app.get("/api/tracing/status")
async def tracing_status():
    return get_langsmith_status()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
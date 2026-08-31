from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
import json
from utils.llm_setup import LLMConfig
from utils.langsmith_config import is_langsmith_enabled
from langsmith import traceable

class RecommendationState(TypedDict):
    student_profile: Dict[str, Any]
    skill_report: Dict[str, Any]
    skill_gaps: List[str]
    recommended_courses: List[Dict]
    recommended_internships: List[Dict]
    recommended_jobs: List[Dict]
    recommended_projects: List[Dict]
    final_recommendations: Dict[str, Any]

class RecommendationAgent:
    def __init__(self):
        self.llm_config = LLMConfig()
        self.main_llm = self.llm_config.get_main_model()
        self.graph = self.build_graph()
    
    def build_graph(self):
        workflow = StateGraph(RecommendationState)
        
        workflow.add_node("analyze_skill_gaps", self.trace_analyze_skill_gaps)
        workflow.add_node("fetch_courses", self.trace_fetch_courses)
        workflow.add_node("fetch_internships", self.trace_fetch_internships)
        workflow.add_node("fetch_jobs", self.trace_fetch_jobs)
        workflow.add_node("fetch_projects", self.trace_fetch_projects)
        workflow.add_node("compile_recommendations", self.trace_compile_recommendations)
        
        workflow.set_entry_point("analyze_skill_gaps")
        workflow.add_edge("analyze_skill_gaps", "fetch_courses")
        workflow.add_edge("analyze_skill_gaps", "fetch_internships")
        workflow.add_edge("analyze_skill_gaps", "fetch_jobs")
        workflow.add_edge("analyze_skill_gaps", "fetch_projects")
        
        workflow.add_edge("fetch_courses", "compile_recommendations")
        workflow.add_edge("fetch_internships", "compile_recommendations")
        workflow.add_edge("fetch_jobs", "compile_recommendations")
        workflow.add_edge("fetch_projects", "compile_recommendations")
        
        workflow.add_edge("compile_recommendations", END)
        
        return workflow.compile()
    
    @traceable(name="recommendation_analyze_gaps", run_type="chain", tags=["recommendation", "skill_gaps"])
    def trace_analyze_skill_gaps(self, state: RecommendationState) -> RecommendationState:
        return self.analyze_skill_gaps(state)
    
    @traceable(name="recommendation_fetch_courses", run_type="chain", tags=["recommendation", "courses"])
    def trace_fetch_courses(self, state: RecommendationState) -> RecommendationState:
        return self.fetch_courses(state)
    
    @traceable(name="recommendation_fetch_internships", run_type="chain", tags=["recommendation", "internships"])
    def trace_fetch_internships(self, state: RecommendationState) -> RecommendationState:
        return self.fetch_internships(state)
    
    @traceable(name="recommendation_fetch_jobs", run_type="chain", tags=["recommendation", "jobs"])
    def trace_fetch_jobs(self, state: RecommendationState) -> RecommendationState:
        return self.fetch_jobs(state)
    
    @traceable(name="recommendation_fetch_projects", run_type="chain", tags=["recommendation", "projects"])
    def trace_fetch_projects(self, state: RecommendationState) -> RecommendationState:
        return self.fetch_projects(state)
    
    @traceable(name="recommendation_compile", run_type="chain", tags=["recommendation", "compile"])
    def trace_compile_recommendations(self, state: RecommendationState) -> RecommendationState:
        return self.compile_recommendations(state)
    
    # Keep all original methods (analyze_skill_gaps, fetch_courses, etc.)
    def analyze_skill_gaps(self, state: RecommendationState) -> RecommendationState:
        skill_report = state["skill_report"]
        skill_gaps = []
        
        for skill, data in skill_report.get("skills", {}).items():
            if data["proficiency"] < 60:
                skill_gaps.append(skill)
        
        state["skill_gaps"] = skill_gaps
        return state
    
    def fetch_courses(self, state: RecommendationState) -> RecommendationState:
        from models.course import Course
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            courses = db.query(Course).all()
            skill_gaps = state["skill_gaps"]
            
            recommended = []
            for course in courses:
                course_skills = json.loads(course.skills_covered) if isinstance(course.skills_covered, str) else course.skills_covered
                matched = set(course_skills) & set(skill_gaps)
                
                if matched:
                    recommended.append({
                        "id": course.id,
                        "title": course.title,
                        "provider": course.provider,
                        "rating": course.rating,
                        "price": course.price,
                        "match_score": round(len(matched) / len(skill_gaps) * 100, 2) if skill_gaps else 0
                    })
            
            recommended.sort(key=lambda x: x["match_score"], reverse=True)
            state["recommended_courses"] = recommended[:5]
        finally:
            db.close()
        
        return state
    
    def fetch_internships(self, state: RecommendationState) -> RecommendationState:
        from models.opportunity import Opportunity, OpportunityType
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            internships = db.query(Opportunity).filter(
                Opportunity.type == OpportunityType.INTERNSHIP,
                Opportunity.is_active == True
            ).all()
            
            student_skills = state["skill_report"].get("skills", {})
            
            recommended = []
            for internship in internships:
                required_skills = json.loads(internship.required_skills) if isinstance(internship.required_skills, str) else internship.required_skills
                
                matched_skills = []
                for req in required_skills:
                    skill_name = req.get("skill", "")
                    required_prof = req.get("proficiency", 50)
                    student_prof = student_skills.get(skill_name, {}).get("proficiency", 0)
                    if student_prof >= required_prof:
                        matched_skills.append(skill_name)
                
                match_score = len(matched_skills) / len(required_skills) * 100 if required_skills else 0
                
                if match_score >= 50:
                    recommended.append({
                        "id": internship.id,
                        "title": internship.title,
                        "company": internship.recruiter.company_name if internship.recruiter else "Unknown",
                        "match_score": round(match_score, 2),
                        "stipend": internship.stipend,
                        "location": internship.location
                    })
            
            recommended.sort(key=lambda x: x["match_score"], reverse=True)
            state["recommended_internships"] = recommended[:5]
        finally:
            db.close()
        
        return state
    
    def fetch_jobs(self, state: RecommendationState) -> RecommendationState:
        from models.opportunity import Opportunity, OpportunityType
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            jobs = db.query(Opportunity).filter(
                Opportunity.type == OpportunityType.JOB,
                Opportunity.is_active == True
            ).all()
            
            student_skills = state["skill_report"].get("skills", {})
            
            recommended = []
            for job in jobs:
                required_skills = json.loads(job.required_skills) if isinstance(job.required_skills, str) else job.required_skills
                
                matched_skills = []
                for req in required_skills:
                    skill_name = req.get("skill", "")
                    required_prof = req.get("proficiency", 50)
                    student_prof = student_skills.get(skill_name, {}).get("proficiency", 0)
                    if student_prof >= required_prof:
                        matched_skills.append(skill_name)
                
                match_score = len(matched_skills) / len(required_skills) * 100 if required_skills else 0
                
                if match_score >= 50:
                    recommended.append({
                        "id": job.id,
                        "title": job.title,
                        "company": job.recruiter.company_name if job.recruiter else "Unknown",
                        "match_score": round(match_score, 2),
                        "stipend": job.stipend,
                        "location": job.location
                    })
            
            recommended.sort(key=lambda x: x["match_score"], reverse=True)
            state["recommended_jobs"] = recommended[:5]
        finally:
            db.close()
        
        return state
    
    def fetch_projects(self, state: RecommendationState) -> RecommendationState:
        from models.course import Project
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            projects = db.query(Project).all()
            skill_gaps = state["skill_gaps"]
            
            recommended = []
            for project in projects:
                project_skills = json.loads(project.skills_taught) if isinstance(project.skills_taught, str) else project.skills_taught
                matched = set(project_skills) & set(skill_gaps)
                
                if matched:
                    recommended.append({
                        "id": project.id,
                        "title": project.title,
                        "difficulty": project.difficulty,
                        "estimated_hours": project.estimated_hours
                    })
            
            state["recommended_projects"] = recommended[:5]
        finally:
            db.close()
        
        return state
    
    def compile_recommendations(self, state: RecommendationState) -> RecommendationState:
        state["final_recommendations"] = {
            "skill_gaps": state["skill_gaps"],
            "courses": state.get("recommended_courses", []),
            "internships": state.get("recommended_internships", []),
            "jobs": state.get("recommended_jobs", []),
            "projects": state.get("recommended_projects", [])
        }
        return state
    
    @traceable(name="recommendation_orchestration", run_type="chain", tags=["recommendation", "orchestration"])
    def get_recommendations(self, student_profile: Dict, skill_report: Dict) -> Dict:
        initial_state = {
            "student_profile": student_profile,
            "skill_report": skill_report,
            "skill_gaps": [],
            "recommended_courses": [],
            "recommended_internships": [],
            "recommended_jobs": [],
            "recommended_projects": [],
            "final_recommendations": {}
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["final_recommendations"]
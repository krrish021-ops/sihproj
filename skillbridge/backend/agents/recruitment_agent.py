from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
import json
from utils.llm_setup import LLMConfig
from utils.langsmith_config import is_langsmith_enabled
from langsmith import traceable

class RecruitmentState(TypedDict):
    opportunity: Dict[str, Any]
    requirements: Dict[str, Any]
    candidates: List[Dict]
    shortlisted: List[Dict]
    ranked_candidates: List[Dict]
    insights: Dict[str, Any]

class RecruitmentAgent:
    def __init__(self):
        self.llm_config = LLMConfig()
        self.main_llm = self.llm_config.get_main_model()
        self.graph = self.build_graph()
    
    def build_graph(self):
        workflow = StateGraph(RecruitmentState)
        
        workflow.add_node("analyze_requirements", self.trace_analyze_requirements)
        workflow.add_node("fetch_candidates", self.trace_fetch_candidates)
        workflow.add_node("match_candidates", self.trace_match_candidates)
        workflow.add_node("rank_candidates", self.trace_rank_candidates)
        workflow.add_node("generate_insights", self.trace_generate_insights)
        
        workflow.set_entry_point("analyze_requirements")
        workflow.add_edge("analyze_requirements", "fetch_candidates")
        workflow.add_edge("fetch_candidates", "match_candidates")
        workflow.add_edge("match_candidates", "rank_candidates")
        workflow.add_edge("rank_candidates", "generate_insights")
        workflow.add_edge("generate_insights", END)
        
        return workflow.compile()
    
    @traceable(name="recruitment_analyze_requirements", run_type="chain", tags=["recruitment", "requirements"])
    def trace_analyze_requirements(self, state: RecruitmentState) -> RecruitmentState:
        return self.analyze_requirements(state)
    
    @traceable(name="recruitment_fetch_candidates", run_type="chain", tags=["recruitment", "candidates"])
    def trace_fetch_candidates(self, state: RecruitmentState) -> RecruitmentState:
        return self.fetch_candidates(state)
    
    @traceable(name="recruitment_match_candidates", run_type="chain", tags=["recruitment", "matching"])
    def trace_match_candidates(self, state: RecruitmentState) -> RecruitmentState:
        return self.match_candidates(state)
    
    @traceable(name="recruitment_rank_candidates", run_type="chain", tags=["recruitment", "ranking"])
    def trace_rank_candidates(self, state: RecruitmentState) -> RecruitmentState:
        return self.rank_candidates(state)
    
    @traceable(name="recruitment_generate_insights", run_type="chain", tags=["recruitment", "insights"])
    def trace_generate_insights(self, state: RecruitmentState) -> RecruitmentState:
        return self.generate_insights(state)
    
    # Keep all original methods
    def analyze_requirements(self, state: RecruitmentState) -> RecruitmentState:
        opportunity = state["opportunity"]
        required_skills = opportunity.get("required_skills", [])
        
        state["requirements"] = {
            "all_skills": required_skills,
            "type": opportunity.get("type", "internship")
        }
        return state
    
    def fetch_candidates(self, state: RecruitmentState) -> RecruitmentState:
        from models.user import StudentProfile, StudentSkill
        from database import SessionLocal
        
        db = SessionLocal()
        try:
            students = db.query(StudentProfile).all()
            
            candidates = []
            for student in students:
                skills = db.query(StudentSkill).filter(
                    StudentSkill.student_id == student.id
                ).all()
                
                candidates.append({
                    "id": student.id,
                    "name": student.user.full_name if student.user else "Unknown",
                    "email": student.user.email if student.user else "",
                    "education": student.education,
                    "skills": [
                        {"skill_name": s.skill_name, "proficiency": s.proficiency}
                        for s in skills
                    ]
                })
            
            state["candidates"] = candidates
        finally:
            db.close()
        
        return state
    
    def match_candidates(self, state: RecruitmentState) -> RecruitmentState:
        requirements = state["requirements"]
        candidates = state["candidates"]
        
        shortlisted = []
        for candidate in candidates:
            candidate_skills = {s["skill_name"]: s for s in candidate["skills"]}
            
            matched_skills = []
            missing_skills = []
            
            for req_skill in requirements["all_skills"]:
                skill_name = req_skill.get("skill", "")
                required_prof = req_skill.get("proficiency", 50)
                
                if skill_name in candidate_skills:
                    actual_prof = candidate_skills[skill_name]["proficiency"]
                    if actual_prof >= required_prof:
                        matched_skills.append(skill_name)
                    else:
                        missing_skills.append(skill_name)
                else:
                    missing_skills.append(skill_name)
            
            match_score = len(matched_skills) / len(requirements["all_skills"]) * 100 if requirements["all_skills"] else 0
            
            if match_score >= 50:
                candidate["match_score"] = round(match_score, 2)
                candidate["matched_skills"] = matched_skills
                candidate["missing_skills"] = missing_skills
                shortlisted.append(candidate)
        
        shortlisted.sort(key=lambda x: x["match_score"], reverse=True)
        state["shortlisted"] = shortlisted
        return state
    
    def rank_candidates(self, state: RecruitmentState) -> RecruitmentState:
        state["ranked_candidates"] = state["shortlisted"][:10]
        return state
    
    def generate_insights(self, state: RecruitmentState) -> RecruitmentState:
        insights = {
            "total_candidates": len(state["candidates"]),
            "shortlisted_count": len(state["shortlisted"]),
            "match_rate": round(len(state["shortlisted"]) / max(len(state["candidates"]), 1) * 100, 2)
        }
        state["insights"] = insights
        return state
    
    @traceable(name="recruitment_orchestration", run_type="chain", tags=["recruitment", "orchestration"])
    def get_candidate_recommendations(self, opportunity: Dict) -> Dict:
        initial_state = {
            "opportunity": opportunity,
            "requirements": {},
            "candidates": [],
            "shortlisted": [],
            "ranked_candidates": [],
            "insights": {}
        }
        
        final_state = self.graph.invoke(initial_state)
        
        return {
            "ranked_candidates": final_state["ranked_candidates"],
            "insights": final_state["insights"]
        }
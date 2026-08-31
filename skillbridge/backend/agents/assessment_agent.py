from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json
import re
from datetime import datetime
from utils.llm_setup import LLMConfig
from utils.langsmith_config import is_langsmith_enabled

# LangSmith imports
from langsmith import traceable
try:
    from langchain_core.callbacks.tracers.langchain import LangChainTracer
    from langchain_core.callbacks.manager import tracing_v2_enabled
except ImportError:
    # Fallback for older versions
    try:
        from langchain.callbacks.tracers.langchain import LangChainTracer
        from langchain.callbacks.manager import tracing_v2_enabled
    except ImportError:
        # If callbacks not available, create dummy classes
        class LangChainTracer:
            def __init__(self, project_name=None):
                pass
        tracing_v2_enabled = None

class QuestionResponse(BaseModel):
    question: str = Field(description="The assessment question")
    options: List[str] = Field(description="List of 4 options")
    correct_answer: str = Field(description="The correct answer")
    explanation: str = Field(description="Explanation for the answer")

class AssessmentState(TypedDict):
    student_id: int
    student_profile: Dict[str, Any]
    skill_map: Dict[str, Dict[str, Any]]
    current_skill: Optional[str]
    difficulty_level: str
    question_history: List[Dict]
    current_question: Optional[Dict]
    student_answer: Optional[str]
    evaluation_result: Optional[Dict]
    assessment_complete: bool
    questions_asked: int
    max_questions: int
    skill_report: Optional[Dict]
    initialized: bool

class AssessmentAgent:
    def __init__(self):
        self.llm_config = LLMConfig()
        self.main_llm = self.llm_config.get_main_model()
        self.fast_llm = self.llm_config.get_fast_model()
        
        # LangSmith tracer - safely initialize
        try:
            self.tracer = LangChainTracer(project_name="skillbridge") if is_langsmith_enabled() else None
        except Exception:
            self.tracer = None
        
        self.graph = self.build_graph()
    
    def build_graph(self):
        workflow = StateGraph(AssessmentState)
        
        # Add nodes with traceable decorators
        workflow.add_node("initialize", self.trace_initialize)
        workflow.add_node("select_skill", self.trace_select_skill)
        workflow.add_node("generate_question", self.trace_generate_question)
        workflow.add_node("evaluate_answer", self.trace_evaluate_answer)
        workflow.add_node("update_skill_map", self.trace_update_skill_map)
        workflow.add_node("check_completion", self.trace_check_completion)
        workflow.add_node("generate_report", self.trace_generate_report)
        
        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "select_skill")
        workflow.add_edge("select_skill", "generate_question")
        workflow.add_edge("generate_question", "evaluate_answer")
        workflow.add_edge("evaluate_answer", "update_skill_map")
        workflow.add_edge("update_skill_map", "check_completion")
        
        workflow.add_conditional_edges(
            "check_completion",
            self.should_continue,
            {
                "continue": "select_skill",
                "complete": "generate_report"
            }
        )
        
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    # Traceable node methods
    @traceable(name="assessment_initialize", run_type="chain", tags=["assessment", "initialization"])
    def trace_initialize(self, state: AssessmentState) -> AssessmentState:
        """Initialize assessment - Traced by LangSmith"""
        return self.initialize_assessment(state)
    
    @traceable(name="assessment_select_skill", run_type="chain", tags=["assessment", "skill_selection"])
    def trace_select_skill(self, state: AssessmentState) -> AssessmentState:
        """Select skill - Traced by LangSmith"""
        return self.select_skill(state)
    
    @traceable(name="assessment_generate_question", run_type="llm", tags=["assessment", "question_generation"])
    def trace_generate_question(self, state: AssessmentState) -> AssessmentState:
        """Generate question - Traced by LangSmith"""
        return self.generate_question(state)
    
    @traceable(name="assessment_evaluate_answer", run_type="llm", tags=["assessment", "evaluation"])
    def trace_evaluate_answer(self, state: AssessmentState) -> AssessmentState:
        """Evaluate answer - Traced by LangSmith"""
        return self.evaluate_answer(state)
    
    @traceable(name="assessment_update_skills", run_type="chain", tags=["assessment", "skill_update"])
    def trace_update_skill_map(self, state: AssessmentState) -> AssessmentState:
        """Update skills - Traced by LangSmith"""
        return self.update_skill_map(state)
    
    @traceable(name="assessment_check_completion", run_type="chain", tags=["assessment", "completion_check"])
    def trace_check_completion(self, state: AssessmentState) -> AssessmentState:
        """Check completion - Traced by LangSmith"""
        return self.check_completion(state)
    
    @traceable(name="assessment_generate_report", run_type="chain", tags=["assessment", "report"])
    def trace_generate_report(self, state: AssessmentState) -> AssessmentState:
        """Generate report - Traced by LangSmith"""
        return self.generate_report(state)
    
    # Original methods (keep as is)
    def initialize_assessment(self, state: AssessmentState) -> AssessmentState:
        student_profile = state.get("student_profile", {})
        skills = student_profile.get("skills", [])
        
        skill_map = {}
        for skill in skills:
            skill_name = skill.get("skill_name", "")
            if skill_name:
                skill_map[skill_name] = {
                    "proficiency": skill.get("proficiency", 50),
                    "confidence": 0.3,
                    "questions_asked": 0,
                    "correct_answers": 0
                }
        
        if not skill_map:
            default_skills = ["Python", "JavaScript", "Problem Solving"]
            for skill in default_skills:
                skill_map[skill] = {
                    "proficiency": 50,
                    "confidence": 0.3,
                    "questions_asked": 0,
                    "correct_answers": 0
                }
        
        state["skill_map"] = skill_map
        state["question_history"] = []
        state["questions_asked"] = 0
        state["max_questions"] = 10
        state["assessment_complete"] = False
        state["initialized"] = True
        
        return state
    
    def select_skill(self, state: AssessmentState) -> AssessmentState:
        skill_map = state["skill_map"]
        min_confidence = float('inf')
        selected_skill = None
        
        for skill, data in skill_map.items():
            if data["questions_asked"] < 4:
                if data["confidence"] < min_confidence:
                    min_confidence = data["confidence"]
                    selected_skill = skill
        
        if not selected_skill:
            selected_skill = list(skill_map.keys())[0]
        
        state["current_skill"] = selected_skill
        
        skill_data = skill_map[selected_skill]
        if skill_data["questions_asked"] > 0:
            accuracy = skill_data["correct_answers"] / skill_data["questions_asked"]
            if accuracy > 0.7:
                state["difficulty_level"] = "advanced"
            elif accuracy > 0.4:
                state["difficulty_level"] = "intermediate"
            else:
                state["difficulty_level"] = "beginner"
        else:
            state["difficulty_level"] = "beginner"
        
        return state
    
    def generate_question(self, state: AssessmentState) -> AssessmentState:
        prompt = f"""You are an expert technical interviewer.
        Generate a {state['difficulty_level']} level multiple choice question about {state['current_skill']}.
        
        Return ONLY JSON in this exact format:
        {{
            "question": "Your question here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "Brief explanation of why this is correct"
        }}
        """
        
        try:
            response = self.main_llm.invoke(prompt)
            content = response.content
            
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                question_data = json.loads(json_match.group())
                state["current_question"] = {
                    "skill": state["current_skill"],
                    "difficulty": state["difficulty_level"],
                    "question": question_data["question"],
                    "options": question_data["options"],
                    "correct_answer": question_data["correct_answer"],
                    "explanation": question_data["explanation"]
                }
            else:
                state["current_question"] = self.get_fallback_question(state)
        except Exception as e:
            state["current_question"] = self.get_fallback_question(state)
        
        return state
    
    def get_fallback_question(self, state):
        return {
            "skill": state["current_skill"],
            "difficulty": state["difficulty_level"],
            "question": f"Rate your proficiency in {state['current_skill']}",
            "options": ["Beginner", "Intermediate", "Advanced", "Expert"],
            "correct_answer": "Intermediate",
            "explanation": "Self-assessment question"
        }
    
    def evaluate_answer(self, state: AssessmentState) -> AssessmentState:
        student_answer = state.get("student_answer", "").strip().lower()
        correct_answer = state["current_question"].get("correct_answer", "").strip().lower()
        
        is_correct = student_answer == correct_answer
        
        if not is_correct and student_answer in ['a', 'b', 'c', 'd']:
            option_index = ord(student_answer) - ord('a')
            if option_index < len(state["current_question"].get("options", [])):
                is_correct = state["current_question"]["options"][option_index].lower() == correct_answer
        
        state["evaluation_result"] = {
            "score": 100 if is_correct else 0,
            "is_correct": is_correct,
            "feedback": "Correct!" if is_correct else "Incorrect."
        }
        
        return state
    
    def update_skill_map(self, state: AssessmentState) -> AssessmentState:
        skill = state["current_skill"]
        skill_data = state["skill_map"][skill]
        
        skill_data["questions_asked"] += 1
        if state["evaluation_result"]["is_correct"]:
            skill_data["correct_answers"] += 1
            skill_data["proficiency"] = min(100, skill_data["proficiency"] + 10)
        else:
            skill_data["proficiency"] = max(0, skill_data["proficiency"] - 5)
        
        skill_data["confidence"] = min(1.0, skill_data["confidence"] + 0.15)
        
        state["question_history"].append({
            "skill": skill,
            "question": state["current_question"]["question"],
            "answer": state["student_answer"],
            "correct": state["evaluation_result"]["is_correct"]
        })
        
        state["questions_asked"] += 1
        
        return state
    
    def should_continue(self, state: AssessmentState) -> str:
        if state["questions_asked"] >= state["max_questions"]:
            return "complete"
        return "continue"
    
    def check_completion(self, state: AssessmentState) -> AssessmentState:
        return state
    
    def generate_report(self, state: AssessmentState) -> AssessmentState:
        skill_report = {
            "skills": {},
            "strengths": [],
            "weaknesses": [],
            "overall_score": 0
        }
        
        total_score = 0
        num_skills = len(state["skill_map"])
        
        for skill, data in state["skill_map"].items():
            skill_report["skills"][skill] = {
                "proficiency": round(data["proficiency"], 2),
                "confidence": round(data["confidence"], 2)
            }
            total_score += data["proficiency"]
            
            if data["proficiency"] >= 70:
                skill_report["strengths"].append(skill)
            elif data["proficiency"] <= 50:
                skill_report["weaknesses"].append(skill)
        
        skill_report["overall_score"] = round(total_score / max(num_skills, 1), 2)
        state["skill_report"] = skill_report
        state["assessment_complete"] = True
        
        return state
    
    @traceable(name="assessment_orchestration", run_type="chain", tags=["assessment", "orchestration"])
    def run_assessment(self, student_id: int, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        initial_state = {
            "student_id": student_id,
            "student_profile": student_profile,
            "skill_map": {},
            "current_skill": None,
            "difficulty_level": "beginner",
            "question_history": [],
            "current_question": None,
            "student_answer": None,
            "evaluation_result": None,
            "assessment_complete": False,
            "questions_asked": 0,
            "max_questions": 10,
            "skill_report": None,
            "initialized": False
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state["skill_report"]
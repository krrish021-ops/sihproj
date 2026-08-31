# Matching Service
from typing import List, Dict, Any
import json

class MatchingService:
    """Service for matching students with opportunities"""
    
    @staticmethod
    def calculate_match_score(student_skills: Dict, required_skills: List) -> float:
        """Calculate match score between student and opportunity"""
        if not required_skills:
            return 0
        
        matched = 0
        for req in required_skills:
            skill_name = req.get("skill", "")
            required_proficiency = req.get("proficiency", 50)
            student_proficiency = student_skills.get(skill_name, {}).get("proficiency", 0)
            
            if student_proficiency >= required_proficiency:
                matched += 1
        
        return (matched / len(required_skills)) * 100
    
    @staticmethod
    def get_matched_skills(student_skills: Dict, required_skills: List) -> List:
        """Get list of matched skills"""
        matched = []
        for req in required_skills:
            skill_name = req.get("skill", "")
            required_proficiency = req.get("proficiency", 50)
            student_proficiency = student_skills.get(skill_name, {}).get("proficiency", 0)
            
            if student_proficiency >= required_proficiency:
                matched.append({
                    "skill": skill_name,
                    "required": required_proficiency,
                    "actual": student_proficiency
                })
        return matched
    
    @staticmethod
    def get_missing_skills(student_skills: Dict, required_skills: List) -> List:
        """Get list of missing skills"""
        missing = []
        for req in required_skills:
            skill_name = req.get("skill", "")
            required_proficiency = req.get("proficiency", 50)
            student_proficiency = student_skills.get(skill_name, {}).get("proficiency", 0)
            
            if student_proficiency < required_proficiency:
                missing.append({
                    "skill": skill_name,
                    "required": required_proficiency,
                    "actual": student_proficiency,
                    "gap": required_proficiency - student_proficiency
                })
        return missing
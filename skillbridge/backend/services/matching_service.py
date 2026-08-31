"""
Skill Matching Service (Assessment-Driven)
=========================================
Prioritizes verified objective assessment scores over self-rated skills.
"""
from typing import List, Dict, Tuple, Optional

def compute_assessment_driven_match(
    self_skills: List[Dict],
    assessed_skills: Optional[Dict[str, int]],
    required_skills: List[Dict]
) -> Tuple[int, List[Dict], List[Dict], bool]:
    """
    Computes match score prioritizing assessment test scores.
    Returns: (score, matched_skills, missing_skills, is_assessment_verified)
    """
    if not required_skills:
        return 0, [], [], False

    self_map = {}
    for s in (self_skills or []):
        name = s.get("skill", "").lower().strip()
        if name:
            self_map[name] = s.get("proficiency", 50)

    test_map = {}
    if assessed_skills:
        for k, v in assessed_skills.items():
            test_map[k.lower().strip()] = int(v)

    has_assessment = len(test_map) > 0
    matched = []
    missing = []
    total_score_weight = 0

    for req in required_skills:
        req_name = req.get("skill", "").strip()
        req_prof = req.get("proficiency", 60)
        if not req_name:
            continue
        req_lower = req_name.lower()

        student_prof = 0
        tested_in_exam = False

        if req_lower in test_map:
            student_prof = test_map[req_lower]
            tested_in_exam = True
        elif req_lower in self_map:
            student_prof = self_map[req_lower]
        else:
            for t_name, t_prof in test_map.items():
                if req_lower in t_name or t_name in req_lower:
                    student_prof = t_prof
                    tested_in_exam = True
                    break
            if student_prof == 0:
                for s_name, s_prof in self_map.items():
                    if req_lower in s_name or s_name in req_lower:
                        student_prof = s_prof
                        break

        entry = {
            "skill": req_name,
            "required": req_prof,
            "yours": student_prof,
            "verified_by_test": tested_in_exam
        }

        if student_prof >= (req_prof * 0.7):
            matched.append(entry)
            total_score_weight += min(100, int((student_prof / max(1, req_prof)) * 100))
        else:
            missing.append(entry)

    raw_score = int(total_score_weight / len(required_skills)) if required_skills else 0
    if has_assessment and raw_score > 0:
        raw_score = min(100, raw_score + 5)

    return raw_score, matched, missing, has_assessment

def compute_match_score(student_skills: List[Dict], required_skills: List[Dict]) -> int:
    score, _, _, _ = compute_assessment_driven_match(student_skills, None, required_skills)
    return score

def compute_match_detailed(student_skills: List[Dict], required_skills: List[Dict]):
    score, matched, missing, _ = compute_assessment_driven_match(student_skills, None, required_skills)
    return score, matched, missing

def merge_skills(self_rated_skills: List[Dict], assessment_skills: Optional[Dict[str, int]] = None) -> List[Dict]:
    merged = {}
    for s in (self_rated_skills or []):
        name = s.get("skill", "").strip()
        if name:
            merged[name.lower()] = {"skill": name, "proficiency": s.get("proficiency", 60), "source": "self_rated"}
    if assessment_skills:
        for name, score in assessment_skills.items():
            merged[name.lower()] = {"skill": name, "proficiency": int(score), "source": "assessment_verified"}
    return list(merged.values())
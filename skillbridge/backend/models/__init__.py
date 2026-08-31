from .user import User, StudentProfile, StudentSkill, StudentProject, RecruiterProfile, AcademicianProfile, UserRole
from .opportunity import Opportunity, Application, OpportunityType
from .assessment import Assessment, Question, StudentAssessment
from .course import Course, Project

__all__ = [
    'User', 'StudentProfile', 'StudentSkill', 'StudentProject',
    'RecruiterProfile', 'AcademicianProfile', 'UserRole',
    'Opportunity', 'Application', 'OpportunityType',
    'Assessment', 'Question', 'StudentAssessment',
    'Course', 'Project'
]
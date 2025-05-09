from typing import *

from pydantic import BaseModel

class EducationUpdateRequest(BaseModel):
    type: str = 'university'
    current_study_year: int
    graduation_year: int
    institution: str
    major: str
    degree_type: str
    gpa: float
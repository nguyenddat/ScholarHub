from typing import *

from pydantic import BaseModel

class EducationDeleteRequest(BaseModel):
    id: str

class EducationCreateRequest(BaseModel):
    type: str = 'university'
    current_study_year: int
    graduation_year: int
    institution: str
    major: str
    degree_type: str
    gpa: float


class EducationUpdateRequest(BaseModel):
    id: str
    type: str = 'university'
    current_study_year: int
    graduation_year: int
    institution: str
    major: str
    degree_type: str
    gpa: float
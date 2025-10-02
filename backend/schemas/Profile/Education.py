from typing import *

from pydantic import BaseModel

class EducationDeleteRequest(BaseModel):
    id: str

class EducationCreateRequest(BaseModel):
    type: str = 'university'
    current_study_year: Optional[int] = None
    graduation_year: Optional[int] = None
    institution: Optional[str] = None
    major: Optional[str] = None
    degree_type: Optional[str] = None
    gpa: Optional[float] = None


class EducationUpdateRequest(BaseModel):
    id: str
    type: Optional[str] = 'university'
    current_study_year: Optional[int] = None
    graduation_year: Optional[int] = None
    institution: Optional[str] = None
    major: Optional[str] = None
    degree_type: Optional[str] = None
    gpa: Optional[float] = None
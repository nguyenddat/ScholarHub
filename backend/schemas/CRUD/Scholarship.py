from typing import *

from pydantic import BaseModel, HttpUrl

class PostScholarshipRequest(BaseModel):
    title: str
    provider: Optional[str] = None
    type: Optional[str] = None
    funding_level: Optional[str] = None
    degree_level: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    major: Optional[str] = None

    # Criteria
    education_criteria: Optional[str] = None
    personal_criteria: Optional[str] = None
    experience_criteria: Optional[str] = None
    research_criteria: Optional[str] = None
    certification_criteria: Optional[str] = None
    achievement_criteria: Optional[str] = None

    # Weights
    weights: Optional[Dict[str, str]] = None

    # Meta
    deadline: Optional[str] = None
    description: Optional[str] = None
    original_url: Optional[str] = None

    class Config:
        from_attributes = True
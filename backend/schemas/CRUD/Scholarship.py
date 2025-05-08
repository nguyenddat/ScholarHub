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
    deadline: Optional[str] = None
    description: Optional[str] = None
    original_url: Optional[str] = None
    language: Optional[str] = None

    class Config:
        from_attributes = True
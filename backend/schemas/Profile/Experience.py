from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class ExperienceDeleteRequest(BaseModel):
    id: int

class ExperienceCreateRequest(BaseModel):
    type: str = Field(default='work')
    title: str
    organization: str
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_ongoing: bool = False
    description: Optional[str] = None

class ExperienceUpdateRequest(BaseModel):
    id: int
    type: str = Field(default='work')
    title: str
    organization: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_ongoing: bool = False
    description: Optional[str] = None
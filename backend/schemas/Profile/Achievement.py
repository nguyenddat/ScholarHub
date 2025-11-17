from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class AchievementDeleteRequest(BaseModel):
    id: int

class AchievementCreateRequest(BaseModel):
    title: str
    issuer: str
    award_date: date
    description: Optional[str] = None

class AchievementUpdateRequest(BaseModel):
    id: int
    title: str
    issuer: str
    award_date: date
    description: Optional[str] = None
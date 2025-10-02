from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class AchievementDeleteRequest(BaseModel):
    id: str

class AchievementCreateRequest(BaseModel):
    title: str
    issuer: str
    award_date: date
    description: Optional[str] = None

class AchievementUpdateRequest(BaseModel):
    id: str
    title: str
    issuer: str
    award_date: date
    description: Optional[str] = None
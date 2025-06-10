from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

class ReferenceDeleteRequest(BaseModel):
    id: str

class ReferenceCreateRequest(BaseModel):
    name: str
    type: Optional[str] = "academic"
    job_title: str
    organization: str
    relationship: str
    email: EmailStr

class ReferenceUpdateRequest(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[str] = None
    job_title: Optional[str] = None
    organization: Optional[str] = None
    relationship: Optional[str] = None
    email: Optional[EmailStr] = None
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class PersonalCreateRequest(BaseModel):
    first_name: Optional[str] = None 
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    job_title: Optional[str] = "student"
    contact_email: Optional[str] = None
    date_of_birth: Optional[str] = str(datetime.today().strftime('%Y-%m-%d'))
    nationality: Optional[str] = None
    country_of_residence: Optional[str] = None
    self_introduction: Optional[str] = None

class PersonalUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    job_title: Optional[str] = None
    contact_email: Optional[str] = None
    date_of_birth: Optional[str] = str(datetime.today().strftime('%Y-%m-%d'))
    nationality: Optional[str] = None
    country_of_residence: Optional[str] = None
    self_introduction: Optional[str] = None

class PersonalDeleteRequest(BaseModel):
    user_id: str
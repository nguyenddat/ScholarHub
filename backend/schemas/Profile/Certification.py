from typing import Optional
from datetime import date

from pydantic import BaseModel


class CertificationDeleteRequest(BaseModel):
    id: str


class CertificationCreateRequest(BaseModel):
    name: str
    type: str
    provider: str
    certification_date: Optional[date] = None
    expiry_date: Optional[date] = None
    image_path: Optional[str] = None
    url: Optional[str] = None

class CertificationUpdateRequest(BaseModel):
    id: str
    name: str
    type: str
    provider: str
    certification_date: Optional[date] = None
    expiry_date: Optional[date] = None
    image_path: Optional[str] = None
    url: Optional[str] = None
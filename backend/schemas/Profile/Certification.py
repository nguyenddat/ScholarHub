from typing import Optional
from datetime import date

from pydantic import BaseModel


class CertificationDeleteRequest(BaseModel):
    id: int


class CertificationCreateRequest(BaseModel):
    name: str
    type: str
    provider: str
    certification_date: Optional[date] = None
    expiry_date: Optional[date] = None
    image_path: Optional[str] = None
    url: Optional[str] = None

class CertificationUpdateRequest(BaseModel):
    id: int
    name: str
    type: str
    provider: str
    certification_date: Optional[date] = None
    expiry_date: Optional[date] = None
    image_path: Optional[str] = None
    url: Optional[str] = None
from typing import *
from pydantic import BaseModel

class DocumentDeleteRequest(BaseModel):
    id: str

class DocumentCreateRequest(BaseModel):
    type: str = 'resume'  # resume, cover_letter, other
    file_path: str
    file_name: Optional[str] = None

class DocumentUpdateRequest(BaseModel):
    id: str
    type: Optional[str] = 'resume'
    file_path: Optional[str] = None
    file_name: Optional[str] = None 
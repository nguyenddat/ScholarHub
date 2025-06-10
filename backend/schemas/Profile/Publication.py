from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class PublicationDeleteRequest(BaseModel):
    id: str

class PublicationCreateRequest(BaseModel):
    title: str
    type: str = Field(default='journal')  # Loại publication, mặc định là 'journal'
    venue_name: str  # Tên nơi công bố (ví dụ: tạp chí, hội nghị...)
    publication_date: Optional[date] = None
    url: Optional[str] = None  # URL của publication, nếu có

class PublicationUpdateRequest(BaseModel):
    id: str  # ID của publication cần cập nhật
    title: Optional[str] = None  # Tiêu đề có thể cập nhật
    type: Optional[str] = None
    venue_name: Optional[str] = None  # Tên nơi công bố có thể cập nhật
    publication_date: Optional[date] = None
    url: Optional[str] = None  # URL của publication có thể cập nhật
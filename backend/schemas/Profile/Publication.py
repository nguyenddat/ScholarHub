from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

class PublicationDeleteRequest(BaseModel):
    id: int

class PublicationCreateRequest(BaseModel):
    title: str
    type: str = Field(default='journal')  # Loại publication, mặc định là 'journal'
    venue_name: str  # Tên nơi công bố (ví dụ: tạp chí, hội nghị...)
    publish_date: date  # Ngày công bố
    url: Optional[str] = None  # URL của publication, nếu có

class PublicationUpdateRequest(BaseModel):
    id: int  # ID của publication cần cập nhật
    title: Optional[str] = None  # Tiêu đề có thể cập nhật
    type: Optional[str] = Field(default='journal')  # Loại publication, mặc định là 'journal'
    venue_name: Optional[str] = None  # Tên nơi công bố có thể cập nhật
    publish_date: Optional[date] = None  # Ngày công bố có thể cập nhật
    url: Optional[str] = None  # URL của publication có thể cập nhật
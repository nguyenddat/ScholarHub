from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    content: str
    image: Optional[str] = None
    video: Optional[str] = None
    files: Optional[List[str]] = []
    post_type: Optional[str] = "general"
    tags: Optional[List[str]] = []

class PostUpdateRequest(BaseModel):
    content: Optional[str] = None
    image: Optional[str] = None
    video: Optional[str] = None
    post_type: Optional[str] = None
    tags: Optional[List[str]] = None

class ReactionRequest(BaseModel):
    reaction_type: str = "like"

class CommentCreateRequest(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: str
    content: str
    image: Optional[str]
    video: Optional[str]
    post_type: str
    tags: List[str]
    created_at: datetime
    author: dict
    reactions: dict  # {"likes": 87, "comments": 32, "reposts": 15}
    user_reacted: bool 
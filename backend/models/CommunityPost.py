from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class CommunityPost(BareBaseModel):
    __tablename__ = 'community_posts'

    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    image = Column(Text, nullable=True)
    video = Column(Text, nullable=True)
    files = Column(JSON, default=list)
    post_type = Column(String(50), default="general")  # experience, announcement, event, question, etc.
    tags = Column(JSON, default=list)  # ["Erasmus+", "StudyAbroad", "ScholarshipTips"]
    repost_of = Column(UUID(as_uuid=True), ForeignKey("community_posts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = relationship("User", back_populates="community_posts")
    reactions = relationship("CommunityReaction", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("CommunityComment", back_populates="post", cascade="all, delete-orphan")
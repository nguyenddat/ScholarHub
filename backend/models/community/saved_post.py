from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.BaseClass import BareBaseModel


class SavedPost(BareBaseModel):
    __tablename__ = 'saved_posts'

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False) 
    saved_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User")
    post = relationship("CommunityPost")

    # Unique constraint - user chỉ save 1 post 1 lần
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='unique_user_post_save'),
    ) 
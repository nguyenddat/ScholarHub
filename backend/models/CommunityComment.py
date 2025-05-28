from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.BaseClass import BareBaseModel, Base

class CommunityComment(BareBaseModel):
    __tablename__ = 'community_comments'

    post_id = Column(UUID(as_uuid=True), ForeignKey("community_posts.id"))
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    post = relationship("CommunityPost", back_populates="comments")
    author = relationship("User") 
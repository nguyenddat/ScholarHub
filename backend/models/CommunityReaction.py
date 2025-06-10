from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.BaseClass import BareBaseModel, Base

class CommunityReaction(BareBaseModel):
    __tablename__ = 'community_reactions'

    post_id = Column(UUID(as_uuid=True), ForeignKey("community_posts.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reaction_type = Column(String(20), default="like")  # like, love, support, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Unique constraint - user can only have one reaction per post
    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='_post_user_reaction'),)

    # Relationships
    post = relationship("CommunityPost", back_populates="reactions")
    user = relationship("User") 
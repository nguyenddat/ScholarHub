from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from models.BaseClass import BareBaseModel

class CommunityCommentReaction(BareBaseModel):
    __tablename__ = 'community_comment_reactions'

    comment_id = Column(Integer, ForeignKey("community_comments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    reaction_type = Column(String(20), default="like")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    comment = relationship("CommunityComment", back_populates="reactions")
    user = relationship("User")

    # Unique constraint: user chỉ reaction 1 lần cho 1 comment
    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='unique_comment_user_reaction'),
    ) 
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from models.BaseClass import BareBaseModel

class Follow(BareBaseModel):
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    followed_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
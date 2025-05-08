from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class CommunityPost(BareBaseModel):
    __tablename__ = 'community_posts'

    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
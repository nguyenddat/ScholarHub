from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, CITEXT

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class UserScholarshipBookmark(Base):
    __tablename__ = 'user_scholarship_bookmarks'
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    scholarship_id = Column(UUID(as_uuid=True), ForeignKey("scholarships.id"), primary_key=True)
    saved_at = Column(DateTime, default=datetime.utcnow)
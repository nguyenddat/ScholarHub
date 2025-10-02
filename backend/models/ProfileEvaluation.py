from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class ProfileEvaluation(BareBaseModel):
    __tablename__ = 'profile_evaluations'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    scholarship_id = Column(UUID(as_uuid=True), ForeignKey("scholarships.id"))
    strengths = Column(Text)
    weaknesses = Column(Text)
    suggestions = Column(Text)
    evaluated_at = Column(DateTime, default=datetime.utcnow)
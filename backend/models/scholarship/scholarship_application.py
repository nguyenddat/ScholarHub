from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, CITEXT

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class ScholarshipApplication(BareBaseModel):
    __tablename__ = 'scholarship_applications'

    user_id = Column(Integer, ForeignKey("users.id"))
    scholarship_id = Column(Integer, ForeignKey("scholarships.id"))
    status = Column(Enum(ApplicationStatusEnum), default=ApplicationStatusEnum.draft)
    submission_date = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.utcnow)
    feedback = Column(Text)

    __table_args__ = (UniqueConstraint('user_id', 'scholarship_id'),)
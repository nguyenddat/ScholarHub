from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, CITEXT

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class UserPoints(Base):
    __tablename__ = 'user_points'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    total_points = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
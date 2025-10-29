from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Connection(Base):
    __tablename__ = 'connections'
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    connected_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    status = Column(Enum(ConnectionStatusEnum), default=ConnectionStatusEnum.pending)
    requested_at = Column(DateTime, default=datetime.utcnow)
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, CITEXT

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Referee(BareBaseModel):
    __tablename__ = 'referees'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(Text)
    type = Column(Text, default='academic')
    job_title = Column(Text)
    organization = Column(Text)
    relationship = Column(Text)
    email = Column(Text)
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Achievement(BareBaseModel):
    __tablename__ = 'achievements'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(Text)
    issuer = Column(Text)
    award_date = Column(Date)
    description = Column(Text)
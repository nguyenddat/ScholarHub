from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Experience(BareBaseModel):
    __tablename__ = 'experiences'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type = Column(Text, default='work')
    title = Column(Text)
    organization = Column(Text)
    location = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    is_ongoing = Column(Boolean, default=False)
    description = Column(Text)
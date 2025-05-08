from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, CITEXT

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Publication(BareBaseModel):
    __tablename__ = 'publications'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(Text)
    type = Column(Text, default='journal')
    venue_name = Column(Text)
    publish_date = Column(Date)
    url = Column(Text)
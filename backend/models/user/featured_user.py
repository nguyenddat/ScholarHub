from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class FeaturedUser(BareBaseModel):
    __tablename__ = 'featured_users'

    user_id = Column(Integer, ForeignKey("users.id"))
    feature_type = Column(Text)
    featured_at = Column(DateTime, default=datetime.utcnow)
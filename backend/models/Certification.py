from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

class Certification(BareBaseModel):
    __tablename__ = 'certifications'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(Text)
    provider = Column(Text)
    certification_date = Column(Date)
    expiry_date = Column(Date)

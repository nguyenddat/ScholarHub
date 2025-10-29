from datetime import date
from sqlalchemy import Column, Text, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from helpers.DictConvert import to_dict
from models.BaseClass import BareBaseModel
from schemas.Profile.Certification import *

class Certification(BareBaseModel):
    __tablename__ = 'certifications'

    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(Text)
    type = Column(Text)
    provider = Column(Text)
    certification_date = Column(Date)
    expiry_date = Column(Date)
    image_path = Column(Text)
    url = Column(Text)
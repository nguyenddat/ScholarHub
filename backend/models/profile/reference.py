from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.BaseClass import BareBaseModel, Base

class Reference(BareBaseModel):
    __tablename__ = 'references'

    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(Text)
    type = Column(Text, default='academic')
    job_title = Column(Text)
    organization = Column(Text)
    relationship = Column(Text)
    email = Column(Text)
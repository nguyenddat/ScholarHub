from sqlalchemy import Column, Integer, Text, ForeignKey, Numeric

from helpers.Enums import *
from models.BaseClass import BareBaseModel

class Education(BareBaseModel):
    __tablename__ = 'educations'

    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Text, default='university')
    current_study_year = Column(Integer)
    graduation_year = Column(Integer)
    institution = Column(Text)
    major = Column(Text)
    degree_type = Column(Text)
    gpa = Column(Numeric(4, 2))
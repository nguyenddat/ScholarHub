from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

default_criteria = {
    "education": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "experience": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "research": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "achievement": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
    "certification": {
        "score": [0, 0, 0, 0, 0],
        "evidence": []
    },
}

class Profile(Base):
    __tablename__ = 'profiles'

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    gender = Column(Text)
    job_title = Column(Text, default='student')
    contact_email = Column(Text)
    date_of_birth = Column(Date)
    nationality = Column(Text)
    country_of_residence = Column(Text)
    self_introduction = Column(Text)

    criteria = Column(Text, default=str(default_criteria))

    is_public = Column(Boolean, default=False)

    user = relationship("User", back_populates="profile")

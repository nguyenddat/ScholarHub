from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

<<<<<<< HEAD
class Profile(Base):
=======
class Profile(BareBaseModel):
>>>>>>> origin/dev_foggo_ben_bo_ho
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
    is_public = Column(Boolean, default=False)

<<<<<<< HEAD
    user = relationship("User", back_populates="profile")
    preferences = relationship("Preference", back_populates="profile")
=======
    user = relationship("User", back_populates="profile")
>>>>>>> origin/dev_foggo_ben_bo_ho

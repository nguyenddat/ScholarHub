from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base
from schemas.Profile.Personal import *

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

    @staticmethod
    def get(db, user):
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        return profile
    
    @staticmethod
    def update(db, user, profile: PersonalUpdateRequest):
        profile_record = db.query(Profile).filter(Profile.user_id == user.id).first()
        try:
            profile_record.first_name = profile.first_name if profile.first_name else profile.first_name
            profile_record.middle_name = profile.middle_name if profile.middle_name else profile.middle_name
            profile_record.last_name = profile.last_name if profile.last_name else profile.last_name
            profile_record.gender = profile.gender if profile.gender else profile.gender
            profile_record.job_title = profile.job_title if profile.job_title else profile.job_title
            profile_record.contact_email = profile.contact_email if profile.contact_email else profile.contact_email
            profile_record.date_of_birth = profile.date_of_birth if profile.date_of_birth else profile.date_of_birth
            profile_record.nationality = profile.nationality if profile.nationality else profile.nationality
            profile_record.country_of_residence = profile.country_of_residence if profile.country_of_residence else profile.country_of_residence
            profile_record.self_introduction = profile.self_introduction if profile.self_introduction else profile.self_introduction

            db.commit()
            db.refresh(profile_record)
            return True, profile_record
        
        except Exception:
            return False, None
    

    @staticmethod
    def create(db, user, profile: PersonalCreateRequest):
        try:
            new_profile = Profile(
                user_id = user.id,
                first_name = profile.first,
                middle_name = profile.middle,
                last_name = profile.last,
                gender = profile.gender,
                job_title = profile.job_title,
                contact_email = profile.contact_email,
                date_of_birth = profile.date_of_birth,
                nationality = profile.nationality,
                country_of_residence = profile.country_of_residence,
                self_introduction = profile.self_introduction
            )

            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            return True, new_profile
        
        except Exception:
            return False, None
        
    
    @staticmethod
    def delete(db, user):
        profile = db.query(Profile).filter(Profile.user_id == user.id).first
        try:
            db.delete(profile)
            db.commit()
            return True
        
        except Exception:
            return False






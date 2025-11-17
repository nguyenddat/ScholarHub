from dateutil.parser import parse
from datetime import date, datetime

from sqlalchemy import Column, Integer, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from helpers.Enums import *
from helpers.DictConvert import to_dict
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

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
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

    criteria = Column(JSONB, default=default_criteria)

    is_public = Column(Boolean, default=False)

    user = relationship("User", back_populates="profile")

    @staticmethod
    def get(db, user):
        profile = db.query(Profile).filter(Profile.user_id == user["id"]).first()
        if not profile:
            return {
                "first_name": None,
                "middle_name": None,
                "last_name": None,
                "gender": None,
                "job_title": None,
                "contact_email": None,
                "date_of_birth": None,
                "nationality": None,
                "country_of_residence": None,
                "self_introduction": None
            }

        else:
            return to_dict(profile)
    
    @staticmethod
    def update(db, user, profile: PersonalUpdateRequest):
        profile_record = db.query(Profile).filter(Profile.user_id == user.id).first()
        dob_raw = profile.date_of_birth

        if isinstance(dob_raw, str):
            dob = parse(dob_raw).date()
        elif isinstance(dob_raw, datetime):
            dob = dob_raw.date()
        elif isinstance(dob_raw, date):
            dob = dob_raw
        else:
            dob = None

        profile_record.first_name = profile.first_name
        profile_record.middle_name = profile.middle_name
        profile_record.last_name = profile.last_name
        profile_record.gender = profile.gender
        profile_record.job_title = profile.job_title
        profile_record.contact_email = profile.contact_email
        profile_record.date_of_birth = dob
        profile_record.nationality = profile.nationality
        profile_record.country_of_residence = profile.country_of_residence
        profile_record.self_introduction = profile.self_introduction

        db.commit()
        db.refresh(profile_record)
        return to_dict(profile_record)
        
    

    @staticmethod
    def create(db, user, profile: PersonalCreateRequest):
        dob_raw = profile.date_of_birth
        if isinstance(dob_raw, str):
            dob = parse(dob_raw).date()
        elif isinstance(dob_raw, datetime):
            dob = dob_raw.date()
        elif isinstance(dob_raw, date):
            dob = dob_raw
        else:
            dob = None


        new_profile = Profile(
            user_id = user.id,
            first_name = profile.first_name,
            middle_name = profile.middle_name,
            last_name = profile.last_name,
            gender = profile.gender,
            job_title = profile.job_title,
            contact_email = profile.contact_email,
            date_of_birth = dob,
            nationality = profile.nationality,
            country_of_residence = profile.country_of_residence,
            self_introduction = profile.self_introduction
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return to_dict(new_profile)
                
    
    @staticmethod
    def delete(db, user):
        profile = db.query(Profile).filter(Profile.user_id == user.id).first()
        try:
            db.delete(profile)
            db.commit()
            return True
        
        except Exception:
            return False

from datetime import datetime

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from helpers.DictConvert import to_dict
from models.BaseClass import BareBaseModel, Base
from schemas.Profile.Experience import ExperienceCreateRequest, ExperienceUpdateRequest, ExperienceDeleteRequest

class Experience(BareBaseModel):
    __tablename__ = 'experiences'

    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Text, default='work')
    title = Column(Text)
    organization = Column(Text)
    location = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    is_ongoing = Column(Boolean, default=False)
    description = Column(Text)

    @staticmethod
    def create(db, user, experience: ExperienceCreateRequest):
        new_exp = Experience(
            user_id=user.id,
            type=experience.type,
            title=experience.title,
            organization=experience.organization,
            location=experience.location,
            start_date=experience.start_date,
            end_date=experience.end_date,
            is_ongoing=experience.is_ongoing,
            description=experience.description
        )
        db.add(new_exp)
        db.commit()
        db.refresh(new_exp)
        return to_dict(new_exp)

    @staticmethod
    def update(db, user, experience: ExperienceUpdateRequest):
        experience_record = db.query(Experience).filter(
            Experience.user_id == user.id,
            Experience.id == experience.id
        ).first()

        if not experience_record:
            return True, None

        experience_record.type = experience.type
        experience_record.title = experience.title
        experience_record.organization = experience.organization
        experience_record.location = experience.location
        experience_record.start_date = experience.start_date
        experience_record.end_date = experience.end_date
        experience_record.is_ongoing = experience.is_ongoing
        experience_record.description = experience.description

        db.commit()
        db.refresh(experience_record)
        return to_dict(experience_record)

    @staticmethod
    def delete(db, user, experience: ExperienceDeleteRequest):
        try:
            exp_record = db.query(Experience).filter(
                Experience.user_id == user.id,
                Experience.id == experience.id
            ).first()

            if exp_record:
                db.delete(exp_record)
                db.commit()
                return True
        except Exception as e:
            return False

    @staticmethod
    def get(db, user, params={}):
        base_query = db.query(Experience).filter(Experience.user_id == user.id)
        if params:
            for key, value in params.items():
                base_query = base_query.filter(getattr(Experience, key) == value)

        experiences = base_query.all()
        return [to_dict(exp) for exp in experiences]
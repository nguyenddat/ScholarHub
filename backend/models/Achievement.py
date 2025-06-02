from datetime import datetime

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
from helpers.DictConvert import to_dict
from models.BaseClass import BareBaseModel, Base
from schemas.Profile.Achievement import *

class Achievement(BareBaseModel):
    __tablename__ = 'achievements'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(Text)
    issuer = Column(Text)
    award_date = Column(Date)
    description = Column(Text)

    @staticmethod
    def create(db, user, achievement: AchievementCreateRequest):
        new_ach = Achievement(
            user_id=user.id,
            title=achievement.title,
            issuer=achievement.issuer,
            award_date=achievement.award_date,
            description=achievement.description
        )
        db.add(new_ach)
        db.commit()
        db.refresh(new_ach)
        return to_dict(new_ach)

    @staticmethod
    def update(db, user, achievement: AchievementUpdateRequest):
        record = db.query(Achievement).filter(
            Achievement.user_id == user.id,
            Achievement.id == achievement.id
        ).first()

        if not record:
            return None

        record.title = achievement.title
        record.issuer = achievement.issuer
        record.award_date = achievement.award_date
        record.description = achievement.description

        db.commit()
        db.refresh(record)
        return to_dict(record)

    @staticmethod
    def delete(db, user, achievement: AchievementDeleteRequest):
        record = db.query(Achievement).filter(
            Achievement.user_id == user.id,
            Achievement.id == achievement.id
        ).first()

        if record:
            db.delete(record)
            db.commit()
            return True

    @staticmethod
    def get(db, user, params={}):
        query = db.query(Achievement).filter(Achievement.user_id == user.id)
        if params:
            for key, value in params.items():
                query = query.filter(getattr(Achievement, key) == value)

        achievements = query.all()
        return [to_dict(a) for a in achievements]
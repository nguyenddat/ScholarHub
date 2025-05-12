from datetime import datetime

from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID

from helpers.Enums import *
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
        try:
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
            return True, {
                "id": str(new_ach.id),
                "title": new_ach.title,
                "issuer": new_ach.issuer,
                "award_date": new_ach.award_date,
                "description": new_ach.description
            }
        except Exception as e:
            return False, str(e)

    @staticmethod
    def update(db, user, achievement: AchievementUpdateRequest):
        try:
            record = db.query(Achievement).filter(
                Achievement.user_id == user.id,
                Achievement.id == achievement.id
            ).first()

            if not record:
                return True, None

            record.title = achievement.title
            record.issuer = achievement.issuer
            record.award_date = achievement.award_date
            record.description = achievement.description

            db.commit()
            db.refresh(record)
            return True, {
                "id": str(record.id),
                "title": record.title,
                "issuer": record.issuer,
                "award_date": record.award_date,
                "description": record.description
            }

        except Exception as err:
            return False, str(err)

    @staticmethod
    def delete(db, user, achievement: AchievementDeleteRequest):
        try:
            record = db.query(Achievement).filter(
                Achievement.user_id == user.id,
                Achievement.id == achievement.id
            ).first()

            if record:
                db.delete(record)
                db.commit()
                return True
        except Exception as e:
            return False

    @staticmethod
    def get(db, user, params={}):
        try:
            query = db.query(Achievement).filter(Achievement.user_id == user.id)
            if params:
                for key, value in params.items():
                    query = query.filter(getattr(Achievement, key) == value)

            achievements = query.all()
            return True, [{
                "id": str(a.id),
                "title": a.title,
                "issuer": a.issuer,
                "award_date": a.award_date,
                "description": a.description
            } for a in achievements]

        except Exception as e:
            return False, str(e)
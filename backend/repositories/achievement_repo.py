from sqlalchemy.orm import Session

from models import Achievement

class AchievementRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        achievements = db.query(Achievement).filter(Achievement.user_id == id).all()
        return achievements
    
    
    @staticmethod
    def create(achievement: Achievement, db: Session):
        db.add(achievement)
        db.flush()
        return achievement
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        achievement = db.query(Achievement).filter(Achievement.id == id).first()
        if not achievement:
            return None
        
        for key, value in update_data.items():
            setattr(achievement, key, value)
        
        db.flush()
        return achievement    
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        achievement = db.query(Achievement).filter(Achievement.id == id).first()
        if not achievement:
            return None

        db.delete(achievement)
    
    @staticmethod
    def toDict(achievement: Achievement, user_id: bool=False):
        res = {
            "id": str(achievement.id),
            "title": achievement.title,
            "issuer": achievement.issuer,
            "award_date": str(achievement.award_date),
            "description": achievement.description
        }
        if user_id:
            res[user_id] = achievement.user_id
        return res
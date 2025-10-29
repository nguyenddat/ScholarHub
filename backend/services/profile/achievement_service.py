from sqlalchemy.orm import Session

from models import Achievement

from repositories import AchievementRepository 

class AchievementService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return AchievementRepository.getByUserId(id, db)

    @staticmethod
    def create(achievement: Achievement, db: Session):
        return AchievementRepository.create(achievement, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return AchievementRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        AchievementRepository.deleteById(id, db)
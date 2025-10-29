from sqlalchemy.orm import Session

from models import Experience

from repositories import ExperienceRepository

class ExperienceService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return ExperienceRepository.getByUserId(id, db)

    @staticmethod
    def create(achievement: Experience, db: Session):
        return ExperienceRepository.create(achievement, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return ExperienceRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        ExperienceRepository.deleteById(id, db)
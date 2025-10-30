from sqlalchemy.orm import Session

from models import Achievement

from repositories import EducationRepository 

class EducationService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return EducationRepository.getByUserId(id, db)

    @staticmethod
    def create(education: Achievement, db: Session):
        return EducationRepository.create(education, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return EducationRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        EducationRepository.deleteById(id, db)
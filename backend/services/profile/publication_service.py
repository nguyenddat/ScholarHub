from sqlalchemy.orm import Session

from models import Publication

from repositories import PublicationRepository

class PublicationService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return PublicationRepository.getByUserId(id, db)

    @staticmethod
    def create(achievement: Publication, db: Session):
        return PublicationRepository.create(achievement, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return PublicationRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        PublicationRepository.deleteById(id, db)
from sqlalchemy.orm import Session

from models import Reference

from repositories import ReferenceRepository

class ReferenceService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return ReferenceRepository.getByUserId(id, db)

    @staticmethod
    def create(reference: Reference, db: Session):
        return ReferenceRepository.create(reference, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return ReferenceRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        ReferenceRepository.deleteById(id, db)
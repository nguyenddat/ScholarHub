from sqlalchemy.orm import Session

from models import Certification

from repositories import CertificationRepository 

class CertificationService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return CertificationRepository.getByUserId(id, db)

    @staticmethod
    def create(certification: Certification, db: Session):
        return CertificationRepository.create(certification, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return CertificationRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        CertificationRepository.deleteById(id, db)
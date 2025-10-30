from sqlalchemy.orm import Session

from models import Document

from repositories import DocumentRepository

class DocumentService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return DocumentRepository.getByUserId(id, db)

    @staticmethod
    def create(certification: Document, db: Session):
        return DocumentRepository.create(certification, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return DocumentRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        DocumentRepository.deleteById(id, db)
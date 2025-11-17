from sqlalchemy.orm import Session

from models import Document

class DocumentRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        documents = db.query(Document).filter(Document.user_id == id).all()
        return [DocumentRepository.toDict(document) for document in documents]
    
    
    @staticmethod
    def create(document: Document, db: Session):
        db.add(document)
        db.flush()
        return document
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        document = db.query(Document).filter(Document.id == id).first()
        if not document:
            return None
        
        for key, value in update_data.items():
            setattr(document, key, value)
        
        db.flush()
        return document
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        document = db.query(Document).filter(Document.id == id).first()
        if not document:
            return None

        db.delete(document)
    
    @staticmethod
    def toDict(document: Document, user_id: bool=False):
        res = {
            'id': document.id,
            "type": document.type,
            "file_path": document.file_path,
            "file_name": document.file_name,
            "uploaded_at": str(document.uploaded_at),
        }
        if user_id:
            res[user_id] = document.user_id
        return res
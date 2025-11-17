from sqlalchemy.orm import Session

from models import Reference

class ReferenceRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        references = db.query(Reference).filter(Reference.user_id == id).all()
        return references
    
    
    @staticmethod
    def create(reference: Reference, db: Session):
        db.add(reference)
        db.flush()
        return reference
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        reference = db.query(Reference).filter(Reference.id == id).first()
        if not reference:
            return None
        
        for key, value in update_data.items():
            setattr(reference, key, value)
        
        db.flush()
        return reference
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        reference = db.query(Reference).filter(Reference.id == id).first()
        if not reference:
            return None

        db.delete(reference)
    
    @staticmethod
    def toDict(reference: Reference, user_id: bool=False):
        res = {
            "id": str(reference.id),
            "name": reference.name,
            "type": reference.type,
            "job_title": reference.job_title,
            "organization": reference.organization,
            "relationship": reference.relationship,
            "email": reference.email,
        }
        if user_id:
            res[user_id] = reference.user_id
        return res
from sqlalchemy.orm import Session

from models import Certification

class CertificationRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        certifications = db.query(Certification).filter(Certification.user_id == id).all()
        return [CertificationRepository.toDict(certification) for certification in certifications]
    
    
    @staticmethod
    def create(certification: Certification, db: Session):
        db.add(certification)
        db.flush()
        return certification
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        certification = db.query(Certification).filter(Certification.id == id).first()
        if not certification:
            return None
        
        for key, value in update_data.items():
            setattr(certification, key, value)
        
        db.flush()
        return certification
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        certification = db.query(Certification).filter(Certification.id == id).first()
        if not certification:
            return None

        db.delete(certification)
    
    @staticmethod
    def toDict(certification: Certification, user_id: bool=False):
        res = {
            "id": str(certification.id),
            "name": certification.name,
            "type": certification.type,
            "provider": certification.provider,
            "certification_date": certification.certification_date,
            "expiry_date": certification.expiry_date,
            "image_path": certification.image_path,
            "url": certification.url,
        }
        if user_id:
            res[user_id] = certification.user_id
        return res
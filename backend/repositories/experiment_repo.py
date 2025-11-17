from sqlalchemy.orm import Session

from models import Experience

class ExperienceRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        experiences = db.query(Experience).filter(Experience.user_id == id).all()
        return experiences
    
    
    @staticmethod
    def create(experience: Experience, db: Session):
        db.add(experience)
        db.flush()
        return experience
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        experience = db.query(Experience).filter(Experience.id == id).first()
        if not experience:
            return None
        
        for key, value in update_data.items():
            setattr(experience, key, value)
        
        db.flush()
        return experience
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        experience = db.query(Experience).filter(Experience.id == id).first()
        if not experience:
            return None

        db.delete(experience)
    
    @staticmethod
    def toDict(experience: Experience, user_id: bool=False):
        res = {
            "id": experience.id,
            "type": experience.type,
            "title": experience.title,
            "organization": experience.organization,
            "location": experience.location,
            "start_date": str(experience.start_date),
            "end_date": str(experience.end_date),
            "is_ongoing": experience.is_ongoing,
            "description": experience.description
        }
        if user_id:
            res[user_id] = experience.user_id
        return res
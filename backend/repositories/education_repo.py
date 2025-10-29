from sqlalchemy.orm import Session

from models import Education

class EducationRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        educations = db.query(Education).filter(Education.user_id == id).all()
        return [EducationRepository.toDict(education) for education in educations]
    
    
    @staticmethod
    def create(education: Education, db: Session):
        db.add(education)
        db.flush()
        return education
    
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        education = db.query(Education).filter(Education.id == id).first()
        if not education:
            return None
        
        for key, value in update_data.items():
            setattr(education, key, value)
        
        db.flush()
        return education
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        education = db.query(Education).filter(Education.id == id).first()
        if not education:
            return None

        db.delete(education)
    
    @staticmethod
    def toDict(education: Education, user_id: bool=False):
        res = {
            "type": education.type, 
            "current_study_year": education.current_study_year,
            "graduation_year": education.graduation_year,
            "institution": education.institution,
            "major": education.major,
            "degree_type": education.degree_type,
            "gpa": float(education.gpa) if education.gpa is not None else None,
            "id": str(education.id)
        }
        if user_id:
            res[user_id] = education.user_id
        return res
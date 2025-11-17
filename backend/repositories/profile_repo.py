from sqlalchemy.orm import Session

from models import Profile

class ProfileRepository:
    @staticmethod
    def getByUserId(id: int, db: Session):
        profile = db.query(Profile).filter(Profile.user_id == id).first()
        return profile
    
    
    @staticmethod
    def create(profile: Profile, db: Session):
        db.add(profile)
        db.flush()
        return profile
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        profile = db.query(Profile).filter(Profile.user_id == id).first()
        if not profile:
            return None
        
        for key, value in update_data.items():
            setattr(profile, key, value)
        
        db.flush()
        return profile
    
    
    @staticmethod
    def deleteById(id: int, db: Session):
        profile = db.query(Profile).filter(Profile.user_id == id).first()
        if not profile:
            return None

        db.delete(profile)
    
    @staticmethod
    def toDict(profile: Profile, user_id: bool=False):
        res = {
            "first_name": profile.first_name,
            "middle_name": profile.middle_name,
            "last_name": profile.last_name,
            "gender": profile.gender,
            "job_title": profile.job_title,
            "contact_email": profile.contact_email,
            "date_of_birth": str(profile.date_of_birth),
            "nationality": profile.nationality,
            "country_of_residence": profile.country_of_residence,
            "self_introduction": profile.self_introduction,
            "criteria": profile.criteria,
            "is_public": profile.is_public,
        }

        if user_id:
            res[user_id] = profile.user_id
        return res
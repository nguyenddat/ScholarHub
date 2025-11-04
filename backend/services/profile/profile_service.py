from sqlalchemy.orm import Session

from models import Profile

from repositories import ProfileRepository

class ProfileService:
    @staticmethod
    def getByUserId(id: int, db: Session):
        return ProfileRepository.getByUserId(id, db)

    @staticmethod
    def create(profile: Profile, db: Session):
        return ProfileRepository.create(profile, db)
    
    @staticmethod
    def update(id: int, update_data: dict, db: Session):
        return ProfileRepository.update(id, update_data, db)
    
    @staticmethod
    def deleteById(id: int, db: Session):
        ProfileRepository.deleteById(id, db)
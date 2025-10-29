from sqlalchemy.orm import Session

from models.Profile import Profile

class ProfileRepository:
    @staticmethod
    def create(profile: Profile, db: Session) -> Profile:
        db.add(profile)
        db.flush()
        return profile
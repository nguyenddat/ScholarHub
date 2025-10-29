from typing import Optional, Union

from sqlalchemy.orm import Session

from models import User

class UserRepository:
    @staticmethod
    def getById(id, db):
        user = db.query(User).filter(User.id == id).first()
        if not user:
            return None

        return user
        
    @staticmethod
    def getByEmail(email: str, db: Session) -> Union[User, None]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None

        return user

    @staticmethod
    def create(user: User, db: Session) -> Union[User, None]:
        db.add(user)
        db.flush()
        return user
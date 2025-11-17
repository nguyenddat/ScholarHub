from typing import Optional, Union

from sqlalchemy.orm import Session

from models import User
from repositories import UserRepository


class UserService:
    @staticmethod
    def getByEmail(email: str, db: Session) -> Union[User, None]:
        return UserService.toDict(UserRepository.getByEmail(email, db))


    @staticmethod
    def getById(id: int, db: Session) -> Union[User, None]:
        return UserService.toDict(UserRepository.getById(id, db))
    
    @staticmethod
    def create(user: User, db: Session):
        return UserService.toDict(UserRepository.create(user, db))

    @staticmethod
    def toDict(user: User):
        res = {
            "id": user.id,
            "email": user.email,
            "password_hash": user.password_hash, 
            "role": user.role,
            "avatar": user.avatar,
            "banner": user.banner,
            "created_at": str(user.created_at),
        }
        return res
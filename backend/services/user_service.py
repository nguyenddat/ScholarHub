from typing import Optional, Union

from sqlalchemy.orm import Session

from models import User
from repositories import UserRepository


class UserService:
    @staticmethod
    def getByEmail(email: str, db: Session) -> Union[User, None]:
        return UserRepository.getByEmail(email, db)


    @staticmethod
    def getById(id: int, db: Session) -> Union[User, None]:
        return UserRepository.getById(id, db)
    
    @staticmethod
    def create(user: User, db: Session):
        return UserRepository.create(user, db)
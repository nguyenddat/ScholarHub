from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship
from fastapi import Depends

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base
from schemas.Auth.auth import UserCreate
from services.Auth.utils import get_password_hash, verify_password

class User(BareBaseModel):
    __tablename__ = 'users'

    email = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user)
    avatar = Column(Text)
    banner = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)

    @staticmethod
    def create_user(db, user: UserCreate):
        """Tạo người dùng mới"""
        check_user = db.query(User).filter(User.email == user.email).first()
        if check_user:
            return False, "Email đã tồn tại"

        if len(user.password) < 8:
            return False, "Mật khẩu phải có ít nhất 8 ký tự"

        new_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password),
            role=UserRoleEnum.user,
            avatar="",
            banner="",
            created_at=str(datetime.utcnow())
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True, {"id": str(new_user.id), "avatar": new_user.avatar, "banner": new_user.banner, "role": new_user.role, "created_at": str(new_user.created_at)}


    @staticmethod
    def authenticate_user(db, email: str, password: str):
        """Xác thực người dùng"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False, "Email không tồn tại"

        if not verify_password(password, user.password_hash):
            return False, "Mật khẩu không chính xác"

        return True, user
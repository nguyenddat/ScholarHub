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
    created_at = Column(DateTime, default=datetime.now())

    profile = relationship("Profile", back_populates="user", uselist=False)
    scholarship = relationship("Scholarship", back_populates="user")
    community_posts = relationship("CommunityPost", back_populates="author")

    @staticmethod
    def create(db, user: UserCreate):
        """Tạo người dùng mới"""
        
        # Kiểm tra người dùng đã tồn tại
        check_user = db.query(User).filter(User.email == user.email).first()
        if check_user: return False, "Email đã tồn tại"
    
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
        return new_user

    @staticmethod
    def authenticate_user(db, email: str, password: str):
        """Xác thực người dùng"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False, "Email không tồn tại"

        if not verify_password(password, user.password_hash):
            return False, "Mật khẩu không chính xác"

        return True, user
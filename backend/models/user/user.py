from datetime import datetime

from sqlalchemy import Column, Text, DateTime, Enum
from sqlalchemy.orm import relationship

from helpers.Enums import *
from models.BaseClass import BareBaseModel, Base

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

    following = relationship("Follow", foreign_keys="[Follow.follower_id]", back_populates="follower", cascade="all, delete-orphan")
    followers = relationship("Follow", foreign_keys="[Follow.followed_id]", back_populates="followed", cascade="all, delete-orphan")
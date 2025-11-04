from typing import List

from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from models import User
from core import settings
from database.init_db import get_db
from services.user_service import UserService
from helpers.Enums import UserRoleEnum
from helpers.security import verifyPassword, createAccessToken, createRefreshToken
from schemas.Auth.auth import RefreshToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
class AuthService:
    @staticmethod
    def authenticate(form_data, db: Session):
        email = form_data.username
        password = form_data.password
        
        user = UserService.getByEmail(email, db)
        if not user:
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
        
        if not verifyPassword(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
        
        access_token = createAccessToken(subject=user.id)
        refresh_token = createRefreshToken(subject=user.id)        
        return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
        }
        
    
    @staticmethod
    def refreshToken(token: RefreshToken, db: Session):
        payload = jwt.decode(token.refresh_token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = UserService.getById(user_id, db)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Tạo token mới
        access_token = createAccessToken(subject=user.id)
        refresh_token = createRefreshToken(subject=user.id)
        return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

    @staticmethod
    def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = UserService.getById(user_id, db)
        if user is None:
            raise credentials_exception
        
        return user


    @staticmethod
    def getCurrentActiveUser() -> User:
        def _get_current_active_user(current_user: User = Depends(AuthService.getCurrentUser)):
            if not current_user:
                raise HTTPException(
                    status_code=401,
                    detail="Inactive user",
                )
            return current_user
        return _get_current_active_user

    @staticmethod
    def adminRequired() -> User:
        def _check_admin_required(current_user: User = Depends(AuthService.getCurrentUser)):
            if not current_user.role == UserRoleEnum.admin:
                raise HTTPException(
                    status_code=403,
                    detail="The user doesn't have enough privileges",
                )
            return current_user
        return _check_admin_required


    @staticmethod
    def checkUserRoles(required_roles: List[UserRoleEnum]):
        def _check_user_role(current_user: User = Depends(AuthService.getCurrentUser)) -> User:
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=403,
                    detail="The user doesn't have enough privileges",
                )
            return current_user
        return _check_user_role
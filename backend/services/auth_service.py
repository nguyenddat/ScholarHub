from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from core import settings
from database.init_db import get_db
from services import UserService
from helpers.security import verifyPassword, createAccessToken, createRefreshToken
from schemas.Auth.auth import RefreshToken, TokenData

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
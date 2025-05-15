from typing import *

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from core.config import settings
from models.User import User
from models.Profile import Profile
from database.init_db import get_db
from schemas.Auth.auth import UserCreate, UserResponse, Token, RefreshToken
from schemas.Profile.Personal import *
from schemas.Profile.Personal import PersonalCreateRequest
from services.Auth.auth import get_current_user
from services.Auth.utils import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/register")
async def register(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> Any:
    
    """Đăng ký người dùng mới"""
    try:
        success, user = User.create_user(db, user_data)        
        if not success:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={        
                    "success": False, 
                    "message": user,
                    "payload": {
                        "user": None
                    },
                }
            )

        else:
            profile = Profile.create(db = db, user = user, profile = PersonalCreateRequest())
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "success": True, 
                    "message": "Đăng ký thành công", 
                    "payload": {
                       "user": user
                    }
                }
            )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False, 
                "message": f"Đã xảy ra lỗi: {str(e)}", 
                "payload": {
                    "user": None
                }
            }
        )


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """Đăng nhập và lấy token"""
    success, user = User.authenticate_user(db, form_data.username, form_data.password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=user,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True, 
            "message": "Đăng nhập thành công",
            "payload": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }}
        )


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    token: RefreshToken, 
    db: Session = Depends(get_db)
) -> Any:
    """Làm mới access token bằng refresh token"""
    try:
        payload = jwt.decode(token.refresh_token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Tạo token mới
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
        "success": True, 
        "message": "Làm mới token thành công",
        "payload": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }}
    )
    

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_user)) -> Any:
    """Lấy thông tin người dùng hiện tại"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True, 
            "message": "Lấy thông tin người dùng thành công",
            "payload": {
                "user": {
                    "id": str(current_user.id),
                    "email": current_user.email,
                    "role": current_user.role,
                    "avatar": current_user.avatar,
                    "banner": current_user.banner,
                    "created_at": str(current_user.created_at)
                }
            }}
    )
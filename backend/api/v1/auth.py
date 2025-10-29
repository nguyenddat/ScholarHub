from typing import *

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models import User, Profile
from database.init_db import get_db
from helpers.DictConvert import to_dict
from schemas.Auth.auth import UserCreate, UserResponse, Token, RefreshToken
from schemas.Profile.Personal import PersonalCreateRequest

from services import AuthService, UserService
from repositories import ProfileRepository

router = APIRouter()

@router.post("/register")
async def register(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> Any:
    """Đăng ký người dùng mới"""
    try:
        user = User(**user_data.dict())
        user = UserService.create(user, db)
        
        # Create blank profile for new user
        profile = Profile(user_id=user.id, **PersonalCreateRequest().dict())
        profile = ProfileRepository(profile, db)
        
        # Commit
        db.commit()
        return JSONResponse({"success": True, "message": "Đăng ký thành công", "payload": to_dict(user)}, 200)

    except Exception as e:
        db.rollback()
        return JSONResponse({"success": False, "message": f"Đã xảy ra lỗi: {str(e)}", "payload": {"user": None}}, 500)


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    try:
        payload = AuthService.authenticate(form_data, db)
        return payload

    except:
        raise HTTPException(500, detail="Xảy ra lỗi khi authenticate")


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    token: RefreshToken, 
    db: Session = Depends(get_db)
) -> Any:
    try:
        payload = AuthService.refreshToken(token, db)
        return payload
    except:
        raise HTTPException(500, detail="Xảy ra lỗi khi refresh token")
    
    
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(AuthService.getCurrentUser)) -> Any:
    """Lấy thông tin người dùng hiện tại"""
    return JSONResponse(
        status_code=200,
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
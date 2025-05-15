from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Achievement import Achievement
from schemas.Profile.Achievement import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager


router = APIRouter()

@router.delete("/achievement")
def delete_achievement(
    payload: AchievementDeleteRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        Achievement.delete(db, user,payload)

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Xóa profile achievement thất bại"
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Xóa profile achievement thành công",
        }
    )

@router.put("/achievement")
def update_achievement(
    payload: AchievementUpdateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user),
):
    try:
        achievement = Achievement.update(
            db = db,
            user = user,
            achievement = payload
        )
    
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = err
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Cập nhật profile achievement thành công",
            "payload": {
                "achievement": achievement
            } 
        }
    )

@router.get("/achievement")
def get_achievement(
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        achievement = Achievement.get(
            db = db,
            user = user,
            params = {}
        )
    
    except Exception as err:
        print(err)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "success": True,
                "message": "Lấy profile achievement thành công",
                "payload": {
                    "achievement": achievement
                }
            }
        )

    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = {
            "success": False,
            "message": "Lấy profile achievement thất bại",
            "payload": achievement
        }
    )

@router.post("/achievement")
def create_achievement(
    payload: AchievementCreateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        achievement = Achievement.create(
            db = db,
            user = user,
            achievement = payload
        )

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = achievement
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {        
            "success": True, 
            "message": "Tạo profile achievement thành công",
            "payload": {
                "achievement": achievement
            },
        }
    )
from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Experience import Experience
from schemas.Profile.Experience import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager


router = APIRouter()

@router.delete("/experience")
def delete_experience(
    payload: ExperienceDeleteRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    success= Experience.delete(
        db = db,
        user = user,
        experience = payload
    )

    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Xóa profile experience thất bại"
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Xóa profile experience thành công",
        }
    )

@router.put("/experience")
def update_experience(
    payload: ExperienceUpdateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user),
):
    try:
        experience = Experience.update(
            db = db,
            user = user,
            experience = payload
        )

        profile_manager.record_request(user.id)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "success": True,
                "message": "Cập nhật profile experience thành công",
                "payload": {
                    "experience": experience
                } 
            }
        )
    
    except Exception as err:
        print(str(err))
        return JSONResponse(
            status_code=500,
            content = {
                "success": False,
                "message": "Cập nhật profile experience thất bại",
                "payload": {
                    "experience": experience
                } 
            }
        )

@router.get("/experience")
def get_experience(
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    experience = Experience.get(
        db = db,
        user = user,
        params = {}
    )

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Lấy profile experience thành công",
            "payload": {
                "experience": experience
            }
        }
    )

@router.post("/experience")
def create_experience(
    payload: ExperienceCreateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    experience = Experience.create(
        db = db,
        user = user,
        experience = payload
    )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {        
                "success": True, 
                "message": "Tạo profile experience thành công",
                "payload": {
                    "experience": experience
                },
            }
        )

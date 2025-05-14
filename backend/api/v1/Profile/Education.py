from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Education import Education
from schemas.Profile.Education import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager

router = APIRouter()

@router.delete("/education")
def delete_education(
    payload: EducationDeleteRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    success= Education.delete(
        db = db,
        user = user,
        education = payload
    )

    profile_manager.record_request(user.id)
    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Xóa profile education thất bại"
        )

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Xóa profile education thành công",
        }
    )

@router.put("/education")
def update_education(
    payload: EducationUpdateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user),
):
    success, education = Education.update(
        db = db,
        user = user,
        education = payload
    )

    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = education
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Cập nhật profile education thành công",
            "payload": {
                "education": education
            } 
        }
    )

@router.get("/education")
def get_education(
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    success, education = Education.get(
        db = db,
        user = user,
        params = {}
    )

    if success:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "success": True,
                "message": "Lấy profile education thành công",
                "payload": {
                    "education": education
                }
            }
        )

    else:
        profile_manager.record_request(user.id)
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "success": False,
                "message": "Lấy profile education thất bại",
                "payload": education
            }
        )

@router.post("/education")
def create_education(
    payload: EducationCreateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    success, education = Education.create(
        db = db,
        user = user,
        education = payload
    )

    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = education
        )

    else:
        profile_manager.record_request(user.id)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {        
                    "success": True, 
                    "message": "Tạo profile education thành công",
                    "payload": {
                        "education": education
                    },
                }
            )
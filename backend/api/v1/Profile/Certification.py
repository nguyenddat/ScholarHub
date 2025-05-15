from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Certification import Certification
from schemas.Profile.Certification import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager


router = APIRouter()

@router.delete("/certification")
def delete_certification(
    payload: CertificationDeleteRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        Certification.delete(db, user, payload)

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Xóa profile certification thất bại"
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Xóa profile certification thành công",
        }
    )

@router.put("/certification")
def update_certification(
    payload: CertificationUpdateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user),
):
    try:
        certification = Certification.update(
            db=db,
            user=user,
            certification=payload
        )

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(err)
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Cập nhật profile certification thành công",
            "payload": {
                "certification": certification
            }
        }
    )

@router.get("/certification")
def get_certification(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        certification = Certification.get(
            db=db,
            user=user,
            params={}
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Lấy profile certification thành công",
                "payload": {
                    "certification": certification
                }
            }
        )

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Lấy profile certification thất bại",
                "payload": None
            }
        )

@router.post("/certification")
def create_certification(
    payload: CertificationCreateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        certification = Certification.create(
            db=db,
            user=user,
            certification=payload
        )

    except Exception as err:
        print(err)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(err)
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Tạo profile certification thành công",
            "payload": {
                "certification": certification
            },
        }
    )
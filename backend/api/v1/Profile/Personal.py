from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Profile import Profile
from schemas.Profile.Personal import *
from services.Auth.auth import get_current_user

router = APIRouter()

@router.post("/personal")
def create_personal(
    payload: PersonalCreateRequest,  # Đổi schema
    db=Depends(get_db),
    user=Depends(get_current_user)
):  
    print(payload.model_dump())
    try:
        result = Profile.create(db=db, user=user, profile=payload)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Tạo personal thành công",
                "payload": {
                    "personal": result
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Tạo personal thất bại",
                "payload": {
                    "personal": str(e)
                }
            }
        )

@router.get("/personal")
def get_personal(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    result = Profile.get(db=db, user=user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy personal thành công",
            "payload": {
                "personal": result
            }
        }
    )

@router.put("/personal")
def update_personal(
    payload: PersonalUpdateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    print(payload.contact_email)
    result = Profile.update(db=db, user=user, profile=payload)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Cập nhật personal thành công",
            "payload": {
                "personal": result
            }
        }
    )

@router.delete("/personal")
def delete_personal(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success = Profile.delete(db=db, user=user)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Xóa personal thất bại"
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Xóa personal thành công"
        }
    )
from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Reference import Reference
from schemas.Profile.Reference import *
from services.Auth.auth import get_current_user

router = APIRouter()

@router.post("/reference")
def create_reference(
    payload: ReferenceCreateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success, result = Reference.create(db=db, user=user, reference=payload)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Tạo reference thất bại",
                "payload": result
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Tạo reference thành công",
            "payload": {
                "reference": result
            }
        }
    )

@router.get("/reference")
def get_references(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success, result = Reference.get(db=db, user=user, params={})

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Lấy reference thất bại",
                "payload": result
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy reference thành công",
            "payload": {
                "reference": result
            }
        }
    )

@router.put("/reference")
def update_reference(
    payload: ReferenceUpdateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success, result = Reference.update(db=db, user=user, reference=payload)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Cập nhật reference thất bại",
                "payload": result
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Cập nhật reference thành công",
            "payload": {
                "reference": result
            }
        }
    )

@router.delete("/reference")
def delete_reference(
    payload: ReferenceDeleteRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success = Reference.delete(db=db, user=user, reference=payload)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Xóa reference thất bại"
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Xóa reference thành công"
        }
    )
from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Publication import Publication
from schemas.Profile.Publication import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager


router = APIRouter()

@router.post("/publication")
def create_publication(
    payload: PublicationCreateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success, result = Publication.create(db=db, user=user, publication=payload)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Tạo publication thất bại",
                "payload": result
            }
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Tạo publication thành công",
            "payload": {
                "publication": result
            }
        }
    )

@router.get("/publication")
def get_publication(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success, result = Publication.get(db=db, user=user, params={})

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Lấy publication thất bại",
                "payload": result
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy publication thành công",
            "payload": {
                "publication": result
            }
        }
    )

@router.put("/publication")
def update_publication(
    payload: PublicationUpdateRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success, result = Publication.update(db=db, user=user, publication=payload)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Cập nhật publication thất bại",
                "payload": result
            }
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Cập nhật publication thành công",
            "payload": {
                "publication": result
            }
        }
    )

@router.delete("/publication")
def delete_publication(
    payload: PublicationDeleteRequest,
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    success = Publication.delete(db=db, user=user, publication=payload)

    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Xóa publication thất bại"
            }
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Xóa publication thành công"
        }
    )
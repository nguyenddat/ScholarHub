from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Document import Document
from schemas.Profile.Document import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager

router = APIRouter()

@router.delete("/document")
def delete_document(
    payload: DocumentDeleteRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    success = Document.delete(
        db = db,
        user = user,
        document = payload
    )

    profile_manager.record_request(user.id)
    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Xóa tài liệu thất bại"
        )

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Xóa tài liệu thành công",
        }
    )

@router.put("/document")
def update_document(
    payload: DocumentUpdateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user),
):
    success, document = Document.update(
        db = db,
        user = user,
        document = payload
    )

    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = document
        )

    profile_manager.record_request(user.id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "success": True,
            "message": "Cập nhật tài liệu thành công",
            "payload": {
                "document": document
            }
        }
    )

@router.get("/document")
def get_documents(
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        documents = Document.get(
            db = db,
            user = user,
            params = {}
        )

        profile_manager.record_request(user.id)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "success": True,
                "message": "Lấy danh sách tài liệu thành công",
                "payload": {
                    "documents": documents
                }
            }
        )

    except Exception as err:
        print(str(err))
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "success": False,
                "message": "Lấy danh sách tài liệu thất bại",
                "payload": str(err)
            }
        )

@router.post("/document")
def create_document(
    payload: DocumentCreateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        document = Document.create(
            db = db,
            user = user,
            document = payload
        )

        profile_manager.record_request(user.id)
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {        
                "success": True,
                "message": "Tạo tài liệu thành công",
                "payload": {
                    "document": document
                },
            }
        )

    except Exception as err:
        print(str(err))
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = str(err)
        ) 
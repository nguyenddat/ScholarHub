from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Document
from schemas.Profile.Document import *
from repositories import DocumentRepository
from services import AuthService, DocumentService, profile_manager

router = APIRouter()

@router.get("/document")
def get_documents(
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        documents = DocumentService.getByUserId(user["id"], db)
        return JSONResponse({"success": True, "message": "Lấy danh sách tài liệu thành công", 
                             "payload": [DocumentRepository.toDict(document) for document in documents]}, 200)

    except:
        raise HTTPException(status_code=500, detail="Lấy danh sách tài liệu thất bại")

@router.post("/document")
def create_document(
    payload: DocumentCreateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        document = Document(user_id=user["id"], **payload.dict())
        document = DocumentService.create(document, db)
        profile_manager.record_request(user["id"])
        
        db.commit()
        db.refresh(document)
        return JSONResponse({"success": True, "message": "Tạo tài liệu thành công", 
                             "payload": DocumentRepository.toDict(document)}, 200)

    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Tạo tài liệu thất bại")

@router.put("/document")
def update_document(
    payload: DocumentUpdateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser),
):
    try:
        document = DocumentService.update(payload.id, payload.dict(exclude={"id"}), db)
        profile_manager.record_request(user["id"])
        
        db.commit()
        db.refresh(document)
        return JSONResponse({"success": True, "message": "Cập nhật tài liệu thành công", 
                             "payload": DocumentRepository.toDict(document)}, 200)
    
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Cập nhật tài liệu thất bại")

@router.delete("/document")
def delete_document(
    payload: DocumentDeleteRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        DocumentService.delete(payload.id, db)
        profile_manager.record_request(user["id"])
        
        db.commit()
        return JSONResponse({"success": True, "message": "Xóa tài liệu thành công"}, 200)

    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Xóa tài liệu thất bại")
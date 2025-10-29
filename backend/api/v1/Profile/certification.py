from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Certification
from schemas.Profile.Certification import *
from services import AuthService, CertificationService
from services.ProfileManager import profile_manager

router = APIRouter()

@router.get("/certification")
def get_certification(
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        certifications = CertificationService.getByUserId(user.id, db)
        return JSONResponse({"success": True, "message": "skibidi", 
                "payload":certifications}, 200)
    except:
        raise HTTPException(500, detail="Xảy ra lỗi khi lấy danh sách certification")


@router.post("/certification")
def create_certification(
    payload: CertificationCreateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        certification = Certification(user_id=user.id, **payload.dict())
        certification = CertificationService.create(certification, db)
        profile_manager.record_request(user.id)
        db.commit()
        db.refresh(certification)
        return JSONResponse({"success": True, "payload": CertificationService.toDict(certification), "message": "skibidi"}, 200)
    except:
        db.rollback()
        raise HTTPException(500, detail="Xảy ra lỗi khi tạo certification")
    

@router.put("/certification")
def update_certification(
    payload: CertificationUpdateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser),
):
    try:
        certification = CertificationService.update(payload.id, **payload.dict(), db=db)
        profile_manager.record_request(user.id)
        db.commit()
        db.refresh(certification)
        return JSONResponse({"success": True, "payload": CertificationService.toDict(certification), "message": "skibidi"}, 200)
    except:
        db.rollback()
        raise HTTPException(500, detail="Xảy ra lỗi khi cập nhật certification")


@router.delete("/certification")
def delete_certification(
    payload: CertificationDeleteRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        CertificationService.deleteById(payload.id, db)
        profile_manager.record_request(user.id)
        db.commit()
        return JSONResponse({"success": True, "payload": {}, "message": "skibidi"}, 200)
    
    except:
        db.rollback()
        raise HTTPException(500, detail="Xảy ra lỗi khi xóa certification")
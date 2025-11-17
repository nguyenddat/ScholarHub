from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Education
from schemas.Profile.Education import *
from repositories import EducationRepository
from services import AuthService, EducationService
from services import profile_manager

router = APIRouter()

@router.get("/education")
def get_education(
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        educations = EducationService.getByUserId(user["id"], db)
        return JSONResponse({"success": True, "message": "skibidi", 
                                "payload": [EducationRepository.toDict(education) for education in educations]}, 200)

    except Exception as err:
        print(str(err))
        raise HTTPException(status_code=500, detail="Lỗi khi lấy thông tin education")


@router.post("/education")
def create_education(
    payload: EducationCreateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        education = Education(user_id=user["id"], **payload.dict())
        education = EducationService.create(education, db)
        profile_manager.record_request(user["id"])
        
        db.commit()
        db.refresh(education)
        
        return JSONResponse({"success": True, "message": "Tạo profile education thành công",
                    "payload": EducationRepository.toDict(education)}, 200)

    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi khi tạo profile education")

@router.put("/education")
def update_education(
    payload: EducationUpdateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser),
):  
    try:
        education = EducationService.update(payload.id, payload.dict(exclude={"id"}), db)
        profile_manager.record_request(user["id"])
        
        db.commit()
        db.refresh(education)

        return JSONResponse({"success": True, "message": "Cập nhật profile education thành công",
                "payload": EducationRepository.toDict(education)}, 200)
    
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi khi cập nhật profile education")


@router.delete("/education")
def delete_education(
    payload: EducationDeleteRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        EducationService.deleteById(payload.id, db)
        profile_manager.record_request(user["id"])
        
        db.commit()
        return JSONResponse({"success": True, "message": "Xóa profile education thành công"}, 200)
    
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Lỗi khi xóa profile education")
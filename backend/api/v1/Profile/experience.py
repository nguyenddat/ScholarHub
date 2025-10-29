from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Experience
from schemas.Profile.Experience import *
from repositories import ExperienceRepository
from services import AuthService, ExperienceService
from services.ProfileManager import profile_manager

router = APIRouter()

@router.get("/experience")
def get_experience(
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        experiences = ExperienceService.getByUserId(user.id, db)
        return JSONResponse({"success": True, "message": "Lấy profile experience thành công", 
                             "payload": ExperienceRepository.toDict(experiences)}, 200)
    
    except Exception as err:
        raise HTTPException(status_code=500, detail="Lấy profile experience thất bại")


@router.post("/experience")
def create_experience(
    payload: ExperienceCreateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        experience = Experience(user_id=user.id, **payload.dict())
        experience = ExperienceService.create(experience, db)
        profile_manager.record_request(user.id)
        
        db.commit()
        db.refresh(experience)
        
        return JSONResponse({"success": True, "message": "Tạo profile experience thành công", 
                             "payload": ExperienceRepository.toDict(experience)}, 200)
    
    except:
        raise HTTPException(status_code=500, detail="Tạo profile experience thất bại")

@router.put("/experience")
def update_experience(
    payload: ExperienceUpdateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser),
):
    try:
        experience = ExperienceService.update(user.id, payload.dict(), db)
        profile_manager.record_request(user.id)
        
        db.commit()
        db.refresh(experience)
        return JSONResponse({"success": True, "message": "Cập nhật profile experience thành công", 
                             "payload": ExperienceRepository.toDict(experience)}, 200)
    
    except:
        raise HTTPException(status_code=500, detail="Cập nhật profile experience thất bại")

@router.delete("/experience")
def delete_experience(
    payload: ExperienceDeleteRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        ExperienceService.delete(user.id, payload.id, db)
        profile_manager.record_request(user.id)
        
        db.commit()
        return JSONResponse({"success": True, "message": "Xoá profile experience thành công"}, 200)

    except:
        raise HTTPException(status_code=500, detail="Xoá profile experience thất bại")
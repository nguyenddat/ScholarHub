from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Achievement
from schemas.Profile.Achievement import *
from repositories import AchievementRepository
from services import AuthService, AchievementService, profile_manager

router = APIRouter()

@router.get("/achievement")
def get_achievement(
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        payload = AchievementService.getByUserId(user.id, db)
        return JSONResponse({"success": True, "payload": payload, "message": "skibidi"}, 200)
    except:
        raise HTTPException(500, detail="Xảy ra lỗi khi lấy danh sách achievement")


@router.post("/achievement")
def create_achievement(
    payload: AchievementCreateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        achievement = Achievement(user_id=user.id, **payload.dict())
        achievement = AchievementService.create(achievement, db)
        profile_manager.record_request(user.id)
        db.commit()
        db.refresh(achievement)
        return JSONResponse({"success": True, "payload": AchievementRepository.toDict(achievement), "message": "skibidi"}, 200)
    except:
        db.rollback()
        raise HTTPException(500, detail="Xảy ra lỗi khi tạo achievement")


@router.put("/achievement")
def update_achievement(
    payload: AchievementUpdateRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser),
):
    try:
        achievement = AchievementService.update(payload.id, **payload.dict(), db=db)
        profile_manager.record_request(user.id)
        db.commit()
        db.refresh(achievement)
        return JSONResponse({"success": True, "payload": AchievementRepository.toDict(achievement), "message": "skibidi"}, 200)
    except:
        db.rollback()
        raise HTTPException(500, detail="Xảy ra lỗi khi cập nhật achievement")    


@router.delete("/achievement")
def delete_achievement(
    payload: AchievementDeleteRequest,
    db = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        AchievementService.deleteById(payload.id, db)
        profile_manager.record_request(user.id)
        db.commit()
        return JSONResponse({"success": True, "payload": {}, "message": "skibidi"}, 200)
    except:
        db.rollback()
        raise HTTPException(500, detail="Xảy ra lỗi khi xóa achievement")    


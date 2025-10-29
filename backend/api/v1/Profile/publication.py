from typing import *

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Publication
from schemas.Profile.Publication import *
from repositories import PublicationRepository
from services import AuthService, PublicationService
from services.ProfileManager import profile_manager

router = APIRouter()

@router.get("/publication")
def get_publication(
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        publications = PublicationService.getByUserId(user.id, db)
        return JSONResponse({"success": True, "message": "Lấy publication thành công", 
                             "payload": [PublicationRepository.toDict(publication) for publication in publications]}, 200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lấy publication thất bại")
        
@router.post("/publication")
def create_publication(
    payload: PublicationCreateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        publication = Publication(user_id=user.id, **payload.dict())
        publication = PublicationService.create(publication, db)
        profile_manager.record_request(user.id)
        
        db.commit()
        db.refresh(publication)
        return JSONResponse({"success": True, "message": "Tạo publication thành công", 
                                "payload": PublicationRepository.toDict(publication)}, 200)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Tạo publication thất bại")


@router.put("/publication")
def update_publication(
    payload: PublicationUpdateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        publication = PublicationService.update(payload.id, payload.dict(exclude={"id"}), db)
        profile_manager.record_request(user.id)
        
        db.commit()
        db.refresh(publication)
        return JSONResponse({"success": True, "message": "Cập nhật publication thành công",
                                "payload": PublicationRepository.toDict(publication)}, 200)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Cập nhật publication thất bại")


@router.delete("/publication")
def delete_publication(
    payload: PublicationDeleteRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        PublicationService.delete(payload.id, db)
        profile_manager.record_request(user.id)
        db.commit()
        
        return JSONResponse({"success": True, "message": "Xóa publication thành công"}, 200)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Xóa publication thất bại")
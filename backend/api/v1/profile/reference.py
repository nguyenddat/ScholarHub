from typing import *

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Reference
from schemas.Profile.Reference import *
from repositories import ReferenceRepository
from services import AuthService, ReferenceService, profile_manager

router = APIRouter()

@router.get("/reference")
def get_references(
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        references = ReferenceService.getByUserId(user["id"], db)
        return JSONResponse({"success": True, "message": "Lấy reference thành công",
                             "payload": [ReferenceRepository.toDict(ref) for ref in references]}, 200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lấy reference thất bại") from e

@router.post("/reference")
def create_reference(
    payload: ReferenceCreateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        reference = Reference(user_id=user["id"], **payload.dict())
        reference = ReferenceService.create(reference, db)
        profile_manager.record_request(user["id"])

        db.commit()
        db.refresh(reference)
        return JSONResponse({"success": True, "message": "Tạo reference thành công",
                             "payload": ReferenceRepository.toDict(reference)}, 200)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Tạo reference thất bại") from e

@router.put("/reference")
def update_reference(
    payload: ReferenceUpdateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        reference = ReferenceService.update(payload.id, payload.dict(exclude={"id"}), db)    
        profile_manager.record_request(user["id"])
        
        db.commit()
        db.refresh(reference)
        return JSONResponse({"success": True, "message": "Cập nhật reference thành công",
                             "payload": ReferenceRepository.toDict(reference)}, 200)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Cập nhật reference thất bại") from e

@router.delete("/reference")
def delete_reference(
    payload: ReferenceDeleteRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        ReferenceService.deleteById(payload.id, db)
        profile_manager.record_request(user["id"])
        db.commit()

        return JSONResponse({"success": True, "message": "Xóa reference thành công"}, 200)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Xóa reference thất bại") from e
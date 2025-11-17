import os
import uuid
from typing import *

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from core import settings
from database.init_db import get_db
from models import User, Follow, Profile
from schemas.Profile.Certification import *
from schemas.Profile.Personal import *
from repositories import ProfileRepository
from services import AuthService, profile_manager, UserService, ProfileService

router = APIRouter()

@router.put("/profile-media/{media_type}")
def update_profile_media(
    media_type: str,
    file: Optional[UploadFile] = File(None),
    db = Depends(get_db),
    current_user: User = Depends(AuthService.getCurrentUser),
):
    if media_type not in ["avatar", "banner"]:
        raise HTTPException(status_code=400, detail="Invalid media type. Use 'avatar' or 'banner'.")
    
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # Tạo thư mục lưu trữ
    save_dir = os.path.join(settings.STATIC_DIR, "profile_media", str(current_user["id"]), media_type)
    os.makedirs(save_dir, exist_ok=True)

    # Đổi tên file để tránh trùng
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(save_dir, filename)
    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        static_return = os.path.join("uploads", "profile_media", str(current_user["id"]), media_type, filename)

        if media_type == "avatar":
            current_user.avatar = static_return
        else:
            current_user.banner = static_return

        db.commit()
        db.refresh(current_user)

        return JSONResponse({"success": True, "file_path": static_return}, 200)

    except Exception as e:
        db.rollback()
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.put("/re-evaluate")
def create_personal(
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):  
    try:
        profile_manager.re_evaluate(db, user["id"])
        return JSONResponse({"success": True, "message": "Đánh giá thành công"}, 200)

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Đánh giá thất bại: {str(err)}")


@router.get("/profile/{user_id}/stats")
def get_profile_stats(
    user_id: str,
    db = Depends(get_db),
    current_user = Depends(AuthService.getCurrentUser)
):
    followers_count = db.query(Follow).filter(Follow.followed_id == user_id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()
    return JSONResponse({"success": True, "message": "Lấy thống kê thành công",
        "payload": {"followers_count": followers_count, "following_count": following_count, "posts_count": 0}}, 200)
    

@router.get("/personal")
def get_personal(
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        profile = ProfileService.getByUserId(user["id"], db)
        return JSONResponse({"success": True, "message": "Lấy personal thành công",
            "payload": ProfileRepository.toDict(profile)}, 200)
    
        
    except:
        raise HTTPException(status_code=500, detail="Lấy personal thất bại")

@router.post("/personal")
def create_personal(
    payload: PersonalCreateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):  
    try:
        profile = Profile(user_id=user["id"], **payload.dict())
        profile = ProfileService.create(profile, db)
        
        db.commit()
        db.refresh(profile)
        return JSONResponse({"success": True, "message": "Tạo personal thành công",
            "payload": ProfileRepository.toDict(profile)}, 200)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Tạo personal thất bại: {str(e)}")

@router.put("/personal")
def update_personal(
    payload: PersonalUpdateRequest,
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    # try:
    profile = ProfileService.update(user["id"], payload.dict(exclude={"id"}), db)
    db.commit()
    db.refresh(profile)
    return JSONResponse({"success": True, "message": "Cập nhật personal thành công",
        "payload": ProfileRepository.toDict(profile)}, 200)
    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail=f"Cập nhật personal thất bại: {str(e)}")

@router.delete("/personal")
def delete_personal(
    db=Depends(get_db),
    user=Depends(AuthService.getCurrentUser)
):
    try:
        ProfileService.deleteById(user["id"], db)
        db.commit()
        return JSONResponse({"success": True, "message": "Xóa personal thành công"}, 200)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Xóa personal thất bại: {str(e)}")
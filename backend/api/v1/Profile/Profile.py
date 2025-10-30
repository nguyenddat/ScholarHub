import os
import uuid
from typing import *

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from core import settings
from database.init_db import get_db
from models import User 
from schemas.Profile.Certification import *
from services import AuthService

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
    save_dir = os.path.join(settings.STATIC_DIR, "profile_media", str(current_user.id), media_type)
    os.makedirs(save_dir, exist_ok=True)

    # Đổi tên file để tránh trùng
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(save_dir, filename)
    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        static_return = os.path.join("uploads", "profile_media", str(current_user.id), media_type, filename)

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

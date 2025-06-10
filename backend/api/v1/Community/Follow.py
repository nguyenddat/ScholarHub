import os
from typing import *

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, APIRouter, Query
from fastapi.responses import JSONResponse

from models.Follow import Follow
from models.User import User
from database.init_db import get_db
from services.Auth.auth import get_current_user

router = APIRouter()

@router.get("/follow")
def get_follows(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    follows = db.query(Follow).filter(
        Follow.follower_id == current_user.id
    ).offset(offset).limit(limit).all()

    result = [
        {
            "user_id": f.followed.id,
            "email": f.email,
            "avatar": f.followed.avatar,
            "banner": f.followed.banner
        }
        for f in follows
    ]

    return JSONResponse(
        status_code=200,
        content={"success": True, "message": "Lấy danh sách follows thành công", "follows": result}
    )

@router.post("/follow")
def follow(
    user_id: str,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    followed_user = db.query(User).filter(User.id == user_id).first()
    if not followed_user:
        return JSONResponse(
            status_code = 400,
            content = {"message": "Không tìm thấy user được follow"}
        )
    
    try:
        new_follow = Follow(
            follower_id = current_user.id,
            followed_id = followed_user.id
        )
        
        db.add(new_follow)
        db.commit()
        db.refresh(new_follow)
        
        return JSONResponse(
            status_code = 201,
            content = {"success": True, "message": "Follow thành công"}
        )
    
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(err)}")


@router.delete("/follow")
def delete_follow(
    user_id: str,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    existed_follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.followed_id == user_id
    ).first()
    if not existed_follow:
        raise HTTPException(status_code=400, detail=f"Không tìm thấy follow")

    try:
        db.delete(existed_follow)
        db.commit()
        
        return JSONResponse(
            status_code = 200,
            content = {"success": True, "message": "Unfollow thành công"}
        )
    
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(err)}")

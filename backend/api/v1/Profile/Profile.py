from typing import *

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from schemas.Profile.Personal import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager

router = APIRouter()

@router.put("/re-evaluate")
def create_personal(
    db=Depends(get_db),
    user=Depends(get_current_user)
):  
    try:
        profile_manager.re_evaluate(db, user.id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Đánh giá thành công",
                "payload": {}
            }
        )

    except Exception as err:
        print(str(err))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": str(err),
                "payload": {}
            }
        )


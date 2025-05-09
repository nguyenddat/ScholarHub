from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Education import Education
from schemas.CRUD.Profile import EducationUpdateRequest
from services.Auth.auth import get_current_user

router = APIRouter()

@router.post("/update-education")
def update_education(
    payload: EducationUpdateRequest,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    success, education = Education.create(
        db = db,
        user = user,
        education = payload
    )

    if not success:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = education
        )

    else:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {        
                    "success": True, 
                    "message": "Tạo profile education thành công",
                    "payload": {
                        "education": education
                    },
                }
            )
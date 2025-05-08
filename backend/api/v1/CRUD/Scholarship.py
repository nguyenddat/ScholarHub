from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Scholarship import Scholarship
from schemas.CRUD.Scholarship import PostScholarshipRequest
from helpers.CriteriaWeights import cal_weights
from services.Auth.auth import get_current_user
from services.CRUD.Scholarship import scholarship_to_description
from ai.ProfileMatching.services.ScholarshipExtract import extract_scholarship

router = APIRouter()


@router.get("/get-scholarships/{suggest}")
def get_scholarship(
    db = Depends(get_db),
    user = Depends(get_current_user),
    suggest: bool = False,
    limit: int = 10,
    offset: int = 0
):
    if not suggest:
        payload = Scholarship.get(
            db = db, 
            mode = "all",
            limit = limit,
            offset = offset
        )
        return JSONResponse(status_code = status.HTTP_200_OK, content = payload)

    else:
        pass



@router.get("/manage-scholarships")
def get_scholarship(
    db = Depends(get_db),
    user = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    try:
        payload = Scholarship.get(
            db = db, 
            mode = "filter",
            params = {"user_id": user.id},
            limit = limit,
            offset = offset
        )
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = payload
        )

    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = str(e)
        )


@router.post("/post-scholarship")
def post_scholarship(
    payload: PostScholarshipRequest, 
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    posted_at = datetime.now()
    data = payload.model_dump()

    weights = cal_weights(data["weights"])
    data.pop("weights")

    for key in weights.keys():
        data[f"{key.split("_")[0]}_weights"] = weights[key]

    scholarship_description = scholarship_to_description(payload)
    scholarship_criteria = extract_scholarship(scholarship_description)
    
    data["user_id"] = user.id
    data["posted_at"] = posted_at
    data["scholarship_criteria"] = str(scholarship_criteria)
    scholarship, success = Scholarship.create(db = db, data = data)
    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = scholarship
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content = scholarship
    )




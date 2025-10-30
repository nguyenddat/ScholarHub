from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import Scholarship
from schemas.CRUD.Scholarship import PostScholarshipRequest
from helpers.CriteriaWeights import cal_weights
from services import get_current_user
from backend.services.retriever_manager import retriever_manager
from services.CRUD.Scholarship import scholarship_to_description
from ai.ProfileMatching.services.ScholarshipExtract import extract_scholarship
from ai.Recommendation.ScholarshipRecommend import recommend_scholarship

router = APIRouter()

@router.get("/scholarships")
def get_scholarship(
    db = Depends(get_db),
    user = Depends(get_current_user),
    suggest: bool = False,
    id: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    if not suggest:
        if id is not None:
            payload = Scholarship.get(db = db, mode = "filter", params = {"id": id})
            if len(payload) > 0:
                payload = payload[0]
        
        else:
            payload = Scholarship.get(db, "all", limit = limit, offset = offset)
    else:
        payload = recommend_scholarship(db = db, user = user)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {        
                "success": True, 
                "message": "Lấy danh sách học bổng thành công",
                "payload": {"scholarships": payload}}
        )


@router.get("/manage-scholarships")
def get_scholarship(
    limit: int = 10,
    offset: int = 0,
    db = Depends(get_db),
    user = Depends(get_current_user),
):
    payload = Scholarship.get(
        db = db, 
        mode = "filter",
        params = {"submitted_by": user.id},
        limit = limit,
        offset = offset
    )
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {        
                "success": True, 
                "message": "Lấy danh sách học bổng thành công",
                "payload": {"scholarships": payload}}
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

    for key, value in weights.items():
        prefix = key.split("_")[0]
        data[f"{prefix}_weights"] = value

    scholarship_description = scholarship_to_description(payload)
    scholarship_criteria = extract_scholarship(scholarship_description)
    
    data["submitted_by"] = user.id
    data["posted_at"] = posted_at
    data["scholarship_criteria"] = scholarship_criteria
    scholarship, success = Scholarship.create(db = db, data = data)
    if not success:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = scholarship
        )
    
    retriever_manager.record_request()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content = {
            "success": True, 
            "message": "Tạo học bổng thành công",
            "payload": {
                "scholarship": scholarship
            },
        } 
    )




from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.Scholarship import Scholarship
from schemas.CRUD.Scholarship import PostScholarshipRequest
from helpers.CriteriaWeights import cal_weights
from services.CRUD.Scholarship import scholarship_to_description
from ai.ProfileMatching.services.ScholarshipExtract import extract_scholarship

router = APIRouter()

@router.get("/get-scholarships")
def get_scholarship(db = Depends(get_db)):
    try:
        payload = Scholarship.get(db = db, mode = "all")
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
def post_scholarship(payload: PostScholarshipRequest, db = Depends(get_db)):
    posted_at = datetime.utcnow()
    data = payload.dict()
    data["posted_at"] = posted_at

    weights = cal_weights(data["weights"])
    data.pop("weights")
    for key in weights.keys():
        data[f"{key}_weights"] = weights[key]

    scholarship_description = scholarship_to_description(payload)
    scholarship_criteria = extract_scholarship(scholarship_description)
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




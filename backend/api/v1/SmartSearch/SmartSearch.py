from fastapi import APIRouter, Depends, status, UploadFile, Form, File
from fastapi.responses import JSONResponse

from database.init_db import get_db
from schemas.SmartSearch.SmartSearch import SmartSearchRequest
from ai.SmartSearch.SmartSearch import search

router = APIRouter()

@router.post("/smart-search")
def smart_search(
    payload: SmartSearchRequest,
    db = Depends(get_db)
):
    try:
        scholarships = search(
            db = db,
            query = payload.query
        )

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "scholarships": scholarships
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "message": str(e)
            }
        )
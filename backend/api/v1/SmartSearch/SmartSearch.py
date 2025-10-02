from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from ai.SmartSearch.SmartSearch import search

router = APIRouter()

@router.get("/smart-search")
def smart_search(
    query: str,
    db = Depends(get_db)
):
    try:
        scholarships = search(
            db = db,
            query = query
        )

        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {        
                    "success": True, 
                    "message": "Lấy danh sách học bổng thành công",
                    "payload": {
                        "scholarships": scholarships
                    },
                }
        )

    
    except Exception as e:
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "message": str(e)
            }
        )
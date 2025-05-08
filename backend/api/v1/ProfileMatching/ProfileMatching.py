import shutil
from datetime import datetime
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, status, UploadFile, Form, File
from fastapi.responses import JSONResponse

from ai.ProfileMatching.ProfileMatching import ResumeMatching

router = APIRouter()

@router.post("/resume-matching")
async def post_scholarship(    
    resume_file: UploadFile = File(...),
    scholarship_description: str = Form(...)
):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp_path = tmp.name
        shutil.copyfileobj(resume_file.file, tmp)
    
    try:
        result = await ResumeMatching(tmp_path, scholarship_description)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": str(e)
            }
        )


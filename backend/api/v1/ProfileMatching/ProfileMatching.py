import shutil
from tempfile import NamedTemporaryFile

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, UploadFile, Form, File, Depends

from database.init_db import get_db
from schemas.CRUD.Scholarship import PostScholarshipRequest
from models import Profile, Education, Experience, Achievement, Publication, Scholarship
from helpers.DictConvert import convert_candidate_to_text, convert_scholarship_to_text
from services.Auth.auth import get_current_user
from ai.core.chain import get_chat_completion
from ai.ProfileMatching.ProfileMatching import resume_matching

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
        result = await resume_matching(tmp_path, scholarship_description)
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


@router.post("/profile-matching")
def profile_matching(
    id: str,
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    scholarship = db.query(Scholarship).filter(Scholarship.id == id).first()
    profile = Profile.get(db, user)
    educations = Education.get(db, user)
    experiences = Experience.get(db, user)
    achievements = Achievement.get(db, user)
    publications = Publication.get(db, user)

    profile = convert_candidate_to_text(profile, educations, experiences, achievements, publications)
    scholarship = convert_scholarship_to_text(scholarship)

    resp = get_chat_completion(
        task = "profile_matching",
        params = {
            "scholarship": scholarship,
            "profile": profile,
            "question": "Evaluate the student's profile against the scholarship description."
        }
    )

    return JSONResponse(
        status_code = 200,
        content = {
            "payload": {
                "success": True,
                "message": "Đánh giá thành công",
                "evaluate": resp 
            }
        }
    )
    
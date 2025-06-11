from typing import *

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from schemas.Profile.Personal import *
from services.Auth.auth import get_current_user
from services.ProfileManager import profile_manager
from models.Profile import Profile
from models.Education import Education
from models.Experience import Experience
from models.Achievement import Achievement
from models.Certification import Certification
from models.Publication import Publication
from models.Reference import Reference
from models.User import User
from models.Follow import Follow

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

@router.get("/me")
def get_current_user_profile(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    """Lấy toàn bộ profile của current user"""
    try:
        # Lấy personal info
        personal = Profile.get(db=db, user=user)
        
        # Lấy education
        education = Education.get(db=db, user=user, params={})
        
        # Lấy experience
        experience = Experience.get(db=db, user=user, params={})
        
        # Lấy achievement
        achievement = Achievement.get(db=db, user=user, params={})
        
        # Lấy certification
        certification = Certification.get(db=db, user=user, params={})
        
        # Lấy publication - FIX: Handle tuple properly
        try:
            pub_result = Publication.get(db=db, user=user, params={})
            if isinstance(pub_result, tuple):
                success, publication = pub_result
                publication = publication if success else []
            else:
                publication = pub_result or []
        except:
            publication = []
            
        # Lấy reference - FIX: Handle tuple properly
        try:
            ref_result = Reference.get(db=db, user=user, params={})
            if isinstance(ref_result, tuple):
                success, reference = ref_result
                reference = reference if success else []
            else:
                reference = ref_result or []
        except:
            reference = []

        # Format response theo IUserProfile interface
        profile_data = {
            "first_name": personal.get("first_name"),
            "middle_name": personal.get("middle_name"),
            "last_name": personal.get("last_name"),
            "gender": personal.get("gender"),
            "job_title": personal.get("job_title"),
            "contact_email": personal.get("contact_email"),
            "date_of_birth": personal.get("date_of_birth"),
            "nationality": personal.get("nationality"),
            "country_of_residence": personal.get("country_of_residence"),
            "self_introduction": personal.get("self_introduction"),
            "educations": education or [],
            "experiences": experience or [],
            "achievements": achievement or [],
            "certifications": certification or [],
            "publications": publication or [],
            "references": reference or [],
            # Thêm các field cho frontend
            "fullName": f"{personal.get('first_name', '')} {personal.get('last_name', '')}".strip() or user.email.split('@')[0],
            "id": str(user.id),
            "avatar": user.avatar if user.avatar else None,  # Lấy từ User model
            "coverImage": None,
            "bio": personal.get("self_introduction"),
            "location": personal.get("country_of_residence"),
            "university": "",  # Có thể lấy từ education đầu tiên
            "major": "",
            "yearOfStudy": None,
            "gpa": None,
            "skills": [],
            "interests": [],
            "socialLinks": {},
            "isPublic": True,
            "createdAt": user.created_at.isoformat() if hasattr(user, 'created_at') else None,
            "updatedAt": user.updated_at.isoformat() if hasattr(user, 'updated_at') else None
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Lấy profile thành công",
                "payload": {
                    "profile": profile_data
                }
            }
        )

    except Exception as e:
        print(f"Error getting profile: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Lấy profile thất bại",
                "payload": {
                    "profile": None
                }
            }
        )

@router.get("/profile/{user_id}/stats")
def get_profile_stats(
    user_id: str,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    followers_count = db.query(Follow).filter(Follow.followed_id == user_id).count()
    following_count = db.query(Follow).filter(Follow.follower_id == user_id).count()
    
    return JSONResponse({
        "success": True,
        "payload": {
            "followers_count": followers_count,
            "following_count": following_count,
            "posts_count": 0  # TODO: Add posts count
        }
    })
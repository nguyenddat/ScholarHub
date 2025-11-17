from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.init_db import get_db
from models import User, Follow
from services import AuthService

router = APIRouter()

@router.get("/connections")
def get_connection_suggestions(
    db: Session = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    try:
        # Lấy danh sách user IDs mà current user đã follow
        followed_user_ids = db.query(Follow.followed_id).filter(
            Follow.follower_id == user["id"]
        ).subquery()
        suggested_users = db.query(User).filter(
            User.id != user["id"],  # Không phải current user
            ~User.id.in_(followed_user_ids)  # Không trong danh sách đã follow
        ).limit(10).all()
        
        suggestions = []
        for suggested_user in suggested_users:
            suggestions.append({
                "id": str(suggested_user.id),
                "name": suggested_user.email.split('@')[0],  # Tạm dùng email prefix
                "role": getattr(suggested_user, 'role', 'user'),
                "avatar": getattr(suggested_user, 'avatar', ''),
                "mutualConnections": 0,  # Tạm thời
                "expertise": ["Essay Writing", "Interview Preparation"],  # Mock data
                "programs": ["Fulbright", "Erasmus+"]  # Mock data
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Lấy gợi ý kết nối thành công",
                "payload": {
                    "connections": suggestions
                }
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi lấy gợi ý kết nối: {str(e)}"
            }
        ) 
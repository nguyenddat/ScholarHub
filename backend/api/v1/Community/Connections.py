from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.init_db import get_db
from models.User import User
from services.Auth.auth import get_current_user

router = APIRouter()

@router.get("/connections")
def get_connection_suggestions(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Lấy gợi ý kết nối - tạm thời trả về random users"""
    try:
        # Lấy một số users khác (không phải current user)
        suggested_users = db.query(User).filter(User.id != user.id).limit(10).all()
        
        suggestions = []
        for suggested_user in suggested_users:
            suggestions.append({
                "id": str(suggested_user.id),
                "name": suggested_user.email.split('@')[0],  # Tạm dùng email prefix
                "role": getattr(suggested_user, 'role', 'Student'),
                "avatar": getattr(suggested_user, 'avatar', '/placeholder.svg?height=48&width=48'),
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
from fastapi import Depends, HTTPException, status
from services.Auth.auth import get_current_user
from models.User import User
from helpers.Enums import UserRoleEnum
from typing import List

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Kiểm tra người dùng hiện tại có hoạt động không"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    return current_user

def admin_required(current_user: User = Depends(get_current_user)) -> User:
    """Kiểm tra người dùng hiện tại có phải là admin không"""
    if not current_user.role == UserRoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

def check_user_role(required_roles: List[UserRoleEnum]):
    """Tạo dependency để kiểm tra quyền của người dùng"""
    def _check_user_role(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges",
            )
        return current_user
    return _check_user_role
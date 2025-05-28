from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.init_db import get_db
from models.CommunityPost import CommunityPost
from models.CommunityReaction import CommunityReaction
from models.CommunityComment import CommunityComment
from models.User import User
from models.Profile import Profile
from schemas.Community.Posts import *
from services.Auth.auth import get_current_user
from models.CommunityCommentReaction import CommunityCommentReaction

router = APIRouter()

@router.get("/posts")
def get_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Lấy danh sách posts với pagination"""
    try:
        offset = (page - 1) * limit
        
        # Query posts với author info và profile
        posts_query = db.query(CommunityPost).join(User).order_by(CommunityPost.created_at.desc())
        total = posts_query.count()
        posts = posts_query.offset(offset).limit(limit).all()
        
        posts_data = []
        for post in posts:
            # Count reactions
            reactions_count = db.query(CommunityReaction).filter(CommunityReaction.post_id == post.id).count()
            comments_count = db.query(CommunityComment).filter(CommunityComment.post_id == post.id).count()
            
            # Check if user reacted
            user_reaction = db.query(CommunityReaction).filter(
                CommunityReaction.post_id == post.id,
                CommunityReaction.user_id == user.id
            ).first()
            
            # Lấy tên hiển thị từ profile hoặc email
            author_name = post.author.email.split('@')[0]  # default
            author_profile = db.query(Profile).filter(Profile.user_id == post.author.id).first()
            
            if author_profile:
                # Tạo full name từ profile
                full_name_parts = [
                    author_profile.first_name,
                    author_profile.middle_name, 
                    author_profile.last_name
                ]
                full_name = " ".join([part for part in full_name_parts if part and part.strip()])
                
                if full_name.strip():  # Nếu có full name
                    author_name = full_name
            
            posts_data.append({
                "id": str(post.id),
                "content": post.content,
                "image": post.image,
                "post_type": post.post_type,
                "tags": post.tags or [],
                "timestamp": _format_timestamp(post.created_at),
                "author": {
                    "name": author_name,
                    "role": getattr(post.author, 'role', 'Student'),
                    "avatar": getattr(post.author, 'avatar', '/placeholder.svg?height=40&width=40')
                },
                "reactions": {
                    "likes": reactions_count,
                    "comments": comments_count,
                    "reposts": 0  # Tạm thời chưa implement
                },
                "userReacted": user_reaction is not None
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Lấy danh sách posts thành công",
                "payload": {
                    "posts": posts_data,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": (total + limit - 1) // limit
                    }
                }
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi lấy posts: {str(e)}"
            }
        )

@router.post("/posts")
def create_post(
    payload: PostCreateRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Tạo post mới"""
    try:
        new_post = CommunityPost(
            author_id=user.id,
            content=payload.content,
            image=payload.image,
            post_type=payload.post_type,
            tags=payload.tags
        )
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Tạo post thành công",
                "payload": {
                    "post": {
                        "id": str(new_post.id),
                        "content": new_post.content,
                        "image": new_post.image,
                        "post_type": new_post.post_type,
                        "tags": new_post.tags
                    }
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi tạo post: {str(e)}"
            }
        )

@router.post("/posts/{post_id}/reaction")
def toggle_reaction(
    post_id: str,
    payload: ReactionRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Toggle reaction (like/unlike)"""
    try:
        # Check if post exists
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": "Post không tồn tại"
                }
            )
        
        # Check existing reaction
        existing_reaction = db.query(CommunityReaction).filter(
            CommunityReaction.post_id == post_id,
            CommunityReaction.user_id == user.id
        ).first()
        
        if existing_reaction:
            # Remove reaction (unlike)
            db.delete(existing_reaction)
            action = "unreacted"
        else:
            # Add reaction (like)
            new_reaction = CommunityReaction(
                post_id=post_id,
                user_id=user.id,
                reaction_type=payload.reaction_type
            )
            db.add(new_reaction)
            action = "reacted"
        
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": f"Đã {action} post",
                "payload": {
                    "action": action,
                    "reaction_type": payload.reaction_type
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi reaction: {str(e)}"
            }
        )

@router.post("/posts/{post_id}/comments/{comment_id}/reaction")
def toggle_comment_reaction(
    post_id: str,
    comment_id: str,
    payload: ReactionRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Toggle comment reaction (like/unlike)"""
    try:
        # Check if comment exists
        comment = db.query(CommunityComment).filter(CommunityComment.id == comment_id).first()
        if not comment:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": "Comment không tồn tại"
                }
            )
        
        # Check existing reaction
        existing_reaction = db.query(CommunityCommentReaction).filter(
            CommunityCommentReaction.comment_id == comment_id,
            CommunityCommentReaction.user_id == user.id
        ).first()
        
        if existing_reaction:
            # Remove reaction (unlike)
            db.delete(existing_reaction)
            action = "unreacted"
        else:
            # Add reaction (like)
            new_reaction = CommunityCommentReaction(
                comment_id=comment_id,
                user_id=user.id,
                reaction_type=payload.reaction_type
            )
            db.add(new_reaction)
            action = "reacted"
        
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": f"Đã {action} comment",
                "payload": {
                    "action": action,
                    "reaction_type": payload.reaction_type
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi reaction comment: {str(e)}"
            }
        )

@router.get("/posts/{post_id}/comments")
def get_comments(
    post_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Lấy comments của post"""
    try:
        comments = db.query(CommunityComment).join(User).filter(
            CommunityComment.post_id == post_id
        ).order_by(CommunityComment.created_at.asc()).all()
        
        comments_data = []
        for comment in comments:
            # Count likes cho comment
            likes_count = db.query(CommunityCommentReaction).filter(CommunityCommentReaction.comment_id == comment.id).count()
            
            # Check if user liked this comment
            user_liked = db.query(CommunityCommentReaction).filter(
                CommunityCommentReaction.comment_id == comment.id,
                CommunityCommentReaction.user_id == user.id
            ).first() is not None
            
            # Lấy tên hiển thị từ profile hoặc email
            author_name = comment.author.email.split('@')[0]  # default
            author_profile = db.query(Profile).filter(Profile.user_id == comment.author.id).first()
            
            if author_profile:
                # Tạo full name từ profile
                full_name_parts = [
                    author_profile.first_name,
                    author_profile.middle_name,
                    author_profile.last_name
                ]
                full_name = " ".join([part for part in full_name_parts if part and part.strip()])
                
                if full_name.strip():  # Nếu có full name
                    author_name = full_name
            
            comments_data.append({
                "id": str(comment.id),
                "content": comment.content,
                "timestamp": _format_timestamp(comment.created_at),
                "author": {
                    "name": author_name,
                    "role": getattr(comment.author, 'role', 'Student'),
                    "avatar": getattr(comment.author, 'avatar', '/placeholder.svg?height=40&width=40')
                },
                "likes": likes_count,
                "userLiked": user_liked
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Lấy comments thành công",
                "payload": {
                    "comments": comments_data
                }
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi lấy comments: {str(e)}"
            }
        )

@router.post("/posts/{post_id}/comments")
def create_comment(
    post_id: str,
    payload: CommentCreateRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Tạo comment mới"""
    try:
        # Check if post exists
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": "Post không tồn tại"
                }
            )
        
        new_comment = CommunityComment(
            post_id=post_id,
            author_id=user.id,
            content=payload.content
        )
        
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Tạo comment thành công",
                "payload": {
                    "comment": {
                        "id": str(new_comment.id),
                        "content": new_comment.content,
                        "timestamp": _format_timestamp(new_comment.created_at)
                    }
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi tạo comment: {str(e)}"
            }
        )

def _format_timestamp(dt: datetime) -> str:
    """Format timestamp giống frontend"""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 7:
        return dt.strftime("%d/%m/%Y")
    elif diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "now" 
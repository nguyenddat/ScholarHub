from typing import Optional, List
from datetime import datetime
import os

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
from models.SavedPost import SavedPost

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
            # Count reactions, comments, AND reposts
            reactions_count = db.query(CommunityReaction).filter(
                CommunityReaction.post_id == post.id,
                CommunityReaction.reaction_type == "like"
            ).count()
            
            comments_count = db.query(CommunityComment).filter(CommunityComment.post_id == post.id).count()
            
            # Count reposts: đếm số post có repost_of = post.id
            reposts_count = db.query(CommunityPost).filter(CommunityPost.repost_of == post.id).count()
            
            # Check if user reacted
            user_reaction = db.query(CommunityReaction).filter(
                CommunityReaction.post_id == post.id,
                CommunityReaction.user_id == user.id,
                CommunityReaction.reaction_type == "like"
            ).first()
            
            # Check if user đã repost (có post nào của user có repost_of = post.id không)
            user_reposted = db.query(CommunityPost).filter(
                CommunityPost.repost_of == post.id,
                CommunityPost.author_id == user.id
            ).first()
            
            # Check if user saved this post
            user_saved = db.query(SavedPost).filter(
                SavedPost.post_id == post.id,
                SavedPost.user_id == user.id
            ).first()
            
            # Handle image URL
            image_url = None
            if post.image:
                if post.image.startswith('http'):
                    image_url = post.image
                else:
                    image_url = f"{post.image}"
            
            # Handle video URL
            video_url = None
            if post.video:
                if post.video.startswith('http'):
                    video_url = post.video
                else:
                    video_url = f"{post.video}"
            
            # Handle files URLs
            files_urls = []
            if post.files:
                for file_url in post.files:
                    if file_url.startswith('http'):
                        files_urls.append(file_url)
                    else:
                        files_urls.append(f"{file_url}")
            
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
                "image": image_url,
                "video": video_url,
                "files": files_urls,
                "post_type": post.post_type,
                "tags": post.tags or [],
                "timestamp": _format_timestamp(post.created_at),
                "author": {
                    "id": str(post.author.id),
                    "name": author_name,
                    "role": getattr(post.author, 'role', 'Student'),
                    "avatar": None
                },
                "reactions": {
                    "likes": reactions_count,
                    "comments": comments_count,
                    "reposts": reposts_count
                },
                "userReacted": user_reaction is not None,
                "userReposted": user_reposted is not None,
                "userSaved": user_saved is not None
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
        print(f"Get posts error: {str(e)}")  # Debug log
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
            video=payload.video,
            files=payload.files,
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
                        "video": new_post.video,
                        "files": new_post.files,
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
                    "id": str(comment.author.id),
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

@router.post("/posts/{post_id}/repost")
def create_repost(
    post_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Tạo repost - tạo post mới từ post gốc"""
    try:
        # Check if post exists
        original_post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        if not original_post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": "Post không tồn tại"
                }
            )
        
        # Check user không phải author của post gốc
        if original_post.author_id == user.id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "message": "Không thể repost bài viết của chính mình"
                }
            )
        
        # Tạo post mới (repost)
        repost = CommunityPost(
            author_id=user.id,
            content=original_post.content,  # Copy content từ post gốc
            image=original_post.image,      # Copy image
            video=original_post.video,      # Copy video
            files=original_post.files,      # Copy files
            post_type=original_post.post_type,
            tags=original_post.tags,
            repost_of=original_post.id      # Reference đến post gốc
        )
        
        db.add(repost)
        db.commit()
        db.refresh(repost)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Đã repost thành công",
                "payload": {
                    "repost_id": str(repost.id),
                    "original_post_id": str(original_post.id)
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi repost: {str(e)}"
            }
        )

@router.post("/posts/{post_id}/save")
def toggle_save_post(
    post_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Toggle save post (save/unsave)"""
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
        
        # Check existing save
        existing_save = db.query(SavedPost).filter(
            SavedPost.post_id == post_id,
            SavedPost.user_id == user.id
        ).first()
        
        if existing_save:
            # Remove save (unsave)
            db.delete(existing_save)
            action = "unsaved"
        else:
            # Add save
            new_save = SavedPost(
                post_id=post_id,
                user_id=user.id
            )
            db.add(new_save)
            action = "saved"
        
        db.commit()
        
        # Get total saved posts count
        saved_count = db.query(SavedPost).filter(SavedPost.user_id == user.id).count()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": f"Đã {action} post",
                "payload": {
                    "action": action,
                    "saved_count": saved_count
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi save post: {str(e)}"
            }
        )

@router.get("/saved-posts")
def get_saved_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Lấy danh sách saved posts của user"""
    try:
        offset = (page - 1) * limit
        
        # Query saved posts của user
        saved_posts_query = db.query(SavedPost).join(CommunityPost).join(User).filter(
            SavedPost.user_id == user.id
        ).order_by(SavedPost.saved_at.desc())
        
        total = saved_posts_query.count()
        saved_posts = saved_posts_query.offset(offset).limit(limit).all()
        
        posts_data = []
        # base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        for saved_post in saved_posts:
            post = saved_post.post
            
            # Count reactions, comments, reposts (giống như GET posts)
            reactions_count = db.query(CommunityReaction).filter(
                CommunityReaction.post_id == post.id,
                CommunityReaction.reaction_type == "like"
            ).count()
            
            comments_count = db.query(CommunityComment).filter(CommunityComment.post_id == post.id).count()
            reposts_count = db.query(CommunityPost).filter(CommunityPost.repost_of == post.id).count()
            
            # Check user reactions
            user_reaction = db.query(CommunityReaction).filter(
                CommunityReaction.post_id == post.id,
                CommunityReaction.user_id == user.id,
                CommunityReaction.reaction_type == "like"
            ).first()
            
            user_reposted = db.query(CommunityPost).filter(
                CommunityPost.repost_of == post.id,
                CommunityPost.author_id == user.id
            ).first()
            
            # Check if user saved this post
            user_saved = db.query(SavedPost).filter(
                SavedPost.post_id == post.id,
                SavedPost.user_id == user.id
            ).first()
            
            # Handle URLs (giống GET posts)
            image_url = None
            if post.image:
                image_url = f"{post.image}" if not post.image.startswith('http') else post.image
            
            video_url = None 
            if post.video:
                video_url = f"{post.video}" if not post.video.startswith('http') else post.video
            
            files_urls = []
            if post.files:
                for file_url in post.files:
                    files_urls.append(f"{file_url}" if not file_url.startswith('http') else file_url)
            
            # Get author name
            author_name = post.author.email.split('@')[0]
            author_profile = db.query(Profile).filter(Profile.user_id == post.author.id).first()
            
            if author_profile:
                full_name_parts = [
                    author_profile.first_name,
                    author_profile.middle_name,
                    author_profile.last_name
                ]
                full_name = " ".join([part for part in full_name_parts if part and part.strip()])
                if full_name.strip():
                    author_name = full_name
            
            posts_data.append({
                "id": str(post.id),
                "content": post.content,
                "image": image_url,
                "video": video_url,
                "files": files_urls,
                "post_type": post.post_type,
                "tags": post.tags or [],
                "timestamp": _format_timestamp(post.created_at),
                "savedAt": _format_timestamp(saved_post.saved_at),  # Thêm thời gian save
                "author": {
                    "id": str(post.author.id),
                    "name": author_name,
                    "role": getattr(post.author, 'role', 'Student'),
                    "avatar": None
                },
                "reactions": {
                    "likes": reactions_count,
                    "comments": comments_count,
                    "reposts": reposts_count
                },
                "userReacted": user_reaction is not None,
                "userReposted": user_reposted is not None,
                "userSaved": user_saved is not None
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Lấy saved posts thành công",
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
                "message": f"Lỗi khi lấy saved posts: {str(e)}"
            }
        )

@router.get("/saved-posts/count")
def get_saved_posts_count(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Lấy số lượng saved posts của user"""
    try:
        count = db.query(SavedPost).filter(SavedPost.user_id == user.id).count()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "payload": {
                    "count": count
                }
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi đếm saved posts: {str(e)}"
            }
        )

@router.post("/posts/{post_id}/delete")
def delete_post(
    post_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """Xóa post (chỉ author mới được xóa)"""
    try:
        post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
        if not post:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "success": False,
                    "message": "Post không tồn tại"
                }
            )

        if post.author_id != user.id:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "success": False,
                    "message": "Bạn không có quyền xóa bài viết này"
                }
            )
        
        saved_posts_deleted = db.query(SavedPost).filter(SavedPost.post_id == post_id).delete()
        reposts_deleted = db.query(CommunityPost).filter(CommunityPost.repost_of == post_id).delete()
        
        db.delete(post)
        db.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Đã xóa bài viết thành công",
                "payload": {
                    "deleted_post_id": str(post_id),
                    "saved_posts_deleted": saved_posts_deleted,
                    "reposts_deleted": reposts_deleted
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Lỗi khi xóa bài viết: {str(e)}"
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
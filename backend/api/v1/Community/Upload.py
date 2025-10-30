import os
import uuid
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.init_db import get_db
from services import AuthService

router = APIRouter()

# Allowed file types
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/mov", "video/avi"}
ALLOWED_FILE_TYPES = {"application/pdf", "text/plain", "application/msword", 
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}

# Max file sizes (bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB  
MAX_FILE_SIZE = 25 * 1024 * 1024   # 25MB

def get_file_category(content_type: str) -> str:
    """Determine file category based on content type"""
    if content_type in ALLOWED_IMAGE_TYPES:
        return "image"
    elif content_type in ALLOWED_VIDEO_TYPES:
        return "video"
    elif content_type in ALLOWED_FILE_TYPES:
        return "file"
    else:
        return "unknown"

async def validate_file(file: UploadFile) -> tuple[str, int]:
    """Validate uploaded file and return category and size"""
    category = get_file_category(file.content_type)
    
    if category == "unknown":
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # Read file content to get actual size
    content = await file.read()
    file_size = len(content)
    
    # Reset file pointer to beginning
    await file.seek(0)
    
    # Check file size
    if category == "image" and file_size > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB)")
    elif category == "video" and file_size > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=400, detail="Video too large (max 100MB)")
    elif category == "file" and file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 25MB)")
    
    return category, file_size

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    """Upload single file (image/video/document)"""
    try:
        # Validate file
        category, file_size = await validate_file(file)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Create category directory
        upload_dir = f"uploads/{category}s"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Read file content and save
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Create full URL for frontend
        from core.config import settings
        # base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        # file_url = f"{base_url}/uploads/{category}s/{unique_filename}"
        file_url = f"/uploads/{category}s/{unique_filename}"
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "File uploaded successfully",
                "payload": {
                    "file_url": file_url,
                    "file_name": file.filename or "unknown",
                    "file_type": category,
                    "content_type": file.content_type,
                    "size": file_size
                }
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {str(e)}")  # Debug log
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Error uploading file: {str(e)}"
            }
        )

@router.post("/upload/multiple")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user = Depends(AuthService.getCurrentUser)
):
    """Upload multiple files"""
    try:
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 files allowed")
        
        uploaded_files = []
        # base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        
        for file in files:
            # Validate file
            category, file_size = await validate_file(file)
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Create category directory
            upload_dir = f"uploads/{category}s"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, unique_filename)
            
            # Read file content and save
            content = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)
            
            # Add to results with full URL
            # file_url = f"{base_url}/uploads/{category}s/{unique_filename}"
            file_url = f"/uploads/{category}s/{unique_filename}"
            uploaded_files.append({
                "file_url": file_url,
                "file_name": file.filename or "unknown",
                "file_type": category,
                "content_type": file.content_type,
                "size": file_size
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": f"Uploaded {len(uploaded_files)} files successfully",
                "payload": {
                    "files": uploaded_files
                }
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Multiple upload error: {str(e)}")  # Debug log
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Error uploading files: {str(e)}"
            }
        ) 
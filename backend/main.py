import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from core import settings
from api.v1.auth import router as Auth_Router

def get_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    
    # Create uploads directory if not exists
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    application.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    application.mount("/profile_media", StaticFiles(directory="uploads/profile_media"), name="profile_media")
    
    application.include_router(Auth_Router, prefix = "/api/v1/auth", tags = ["Auth"])
    return application

app = get_application()
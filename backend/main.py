from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
import os

from core.config import settings

from api.v1.Profile import (
    Education as education_router,
    Experience as experience_router,
    Achievement as achievement_router,
    Publication as publication_router,
    Reference as reference_router,
    Personal as personal_router,
    Profile as profile_router,
    Certification as certification_router
)

from api.v1.Auth.auth import router as Auth_Router
from api.v1.CRUD.Scholarship import router as CRUD_Scholarship_Router
from api.v1.ProfileMatching.ProfileMatching import router as ProfileMatching_Router
from api.v1.SmartSearch.SmartSearch import router as SmartSearch_Router
from api.v1.chat.routes import router as Chatbot_Router
from api.v1.Community import Posts as community_posts_router
from api.v1.Community import Connections as community_connections_router
from api.v1.Community import Upload as community_upload_router
from api.v1.Profile.Document import router as document_router


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
    
    # Serve static files
    application.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    
    application.include_router(Auth_Router, prefix = "/api/v1/auth", tags = ["Auth"])
    application.include_router(CRUD_Scholarship_Router, prefix = "/api/v1", tags = ["CRUD"])
    application.include_router(ProfileMatching_Router, prefix = "/api/v1/ai", tags = ["Profile Matching"])
    application.include_router(SmartSearch_Router, prefix = "/api/v1/ai", tags = ["Smart Search"])
    application.include_router(Chatbot_Router, prefix = "/api/v1/ai", tags = ["Chatbot"])

    # Profile section
    application.include_router(education_router.router, prefix = "/api/v1/user", tags = ["User - Education"])
    application.include_router(experience_router.router, prefix = "/api/v1/user", tags = ["User - Experience"])
    application.include_router(achievement_router.router, prefix = "/api/v1/user", tags = ["User - Achievement"])
    application.include_router(publication_router.router, prefix = "/api/v1/user", tags = ["User - Publication"])
    application.include_router(reference_router.router, prefix = "/api/v1/user", tags = ["User - Reference"])
    application.include_router(personal_router.router, prefix = "/api/v1/user", tags = ["User - Personal"])
    application.include_router(profile_router.router, prefix = "/api/v1/user", tags = ["User - Profile"])
    application.include_router(certification_router.router, prefix = "/api/v1/user", tags = ["User - Certification"])

    # Community section
    application.include_router(community_posts_router.router, prefix="/api/v1/community", tags=["Community - Posts"])
    application.include_router(community_connections_router.router, prefix="/api/v1/community", tags=["Community - Connections"])
    application.include_router(community_upload_router.router, prefix="/api/v1/community", tags=["Community - Upload"])

    # Thêm vào phần routes
    application.include_router(document_router, prefix="/api/v1/profile", tags=["Documents"])

    return application

app = get_application()
# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)
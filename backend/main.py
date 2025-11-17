import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_ENDPOINT"] = ""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from core import settings
from api.v1 import auth, profile_matching, scholarship, smart_search
from api.v1.profile import achievement, certification, document, education, experience, profile, \
    publication, reference
from api.v1.community import Connections, Follow, Posts, Upload

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
    
    # Routers
    application.include_router(auth.router, prefix = "/api/v1/auth", tags = ["Auth"])    
    application.include_router(scholarship.router, prefix = "/api/v1/scholarships", tags = ["Scholarship"])
    
    application.include_router(profile.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(education.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(experience.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(achievement.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(certification.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(publication.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(reference.router, prefix = "/api/v1/user", tags = ["Profile"])
    application.include_router(document.router, prefix = "/api/v1/user", tags = ["Profile"])
    
    application.include_router(Connections.router, prefix = "/api/v1/community", tags = ["Community"])
    application.include_router(Follow.router, prefix = "/api/v1/community", tags = ["Community"])
    application.include_router(Posts.router, prefix = "/api/v1/community", tags = ["Community"])
    application.include_router(Upload.router, prefix = "/api/v1/community", tags = ["Community"])    

    application.include_router(smart_search.router, prefix = "/api/v1/ai", tags = ["AI"])
    application.include_router(profile_matching.router, prefix = "/api/v1/ai", tags = ["AI"])
    return application

app = get_application()
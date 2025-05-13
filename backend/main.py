from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

from api.v1.Profile import (
    Education as education_router,
    Experience as experience_router,
    Achievement as achievement_router,
    Publication as publication_router,
    Reference as reference_router
)

from api.v1.Auth.auth import router as Auth_Router
from api.v1.CRUD.Scholarship import router as CRUD_Scholarship_Router
from api.v1.ProfileMatching.ProfileMatching import router as ProfileMatching_Router
from api.v1.chat.routes import router as api_router
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
    application.include_router(Auth_Router, prefix = "/api/v1/auth", tags = ["Auth"])
    application.include_router(CRUD_Scholarship_Router, prefix = "/api/v1", tags = ["CRUD"])
    application.include_router(ProfileMatching_Router, prefix = "/api/v1/ai", tags = ["Profile Matching"])
    application.include_router(api_router, prefix = "/api/v1/chat", tags = ["Chat"])

    # Profile section
    application.include_router(education_router.router, prefix = "/api/v1/user", tags = ["User - Education"])
    application.include_router(experience_router.router, prefix = "/api/v1/user", tags = ["User - Experience"])
    application.include_router(achievement_router.router, prefix = "/api/v1/user", tags = ["User - Achievement"])
    application.include_router(publication_router.router, prefix = "/api/v1/user", tags = ["User - Publication"])
    application.include_router(reference_router.router, prefix = "/api/v1/user", tags = ["User - Reference"])

    return application

app = get_application()
# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)
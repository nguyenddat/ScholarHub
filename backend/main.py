from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from api.v1.Auth.auth import router as Auth_Router
from api.v1.CRUD.Scholarship import router as CRUD_Scholarship_Router
from api.v1.ProfileMatching.ProfileMatching import router as ProfileMatching_Router

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
    application.include_router(CRUD_Scholarship_Router, prefix = "/api/v1/crud", tags = ["CRUD"])
    application.include_router(ProfileMatching_Router, prefix = "/api/v1/ai", tags = ["Profile Matching"])

    return application

app = get_application()
# if __name__ == '__main__':
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload = True)
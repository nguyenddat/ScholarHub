import os
from typing import *

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    """
    Settings for the application.
    """
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECURITY_ALGORITHM: str = os.getenv("SECURITY_ALGORITHM", "")
    
    DATABASE_URL: str = os.getenv("DB_URL",  "")

    CRAWL_URL: str = os.getenv("CRAWL_URL")
    CRAWL_API_KEY: str = os.getenv("CRAWL_API_KEY")

    OPENAPI_API_KEY: str = os.getenv("OPENAPI_API_KEY")


settings = Settings()

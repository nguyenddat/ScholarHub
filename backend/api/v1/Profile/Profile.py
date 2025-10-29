from typing import *

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from database.init_db import get_db
from schemas.Profile.Personal import *
from services import UserService
from models import User, Follow
from models import Profile, Education, Experience, Achievement, Certification, Publication, Reference

router = APIRouter()
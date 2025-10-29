from typing import Union, Any, Optional
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verifyPassword(plain_password: str, hashed_password: str) -> bool:
    global pwd_context
    return pwd_context.verify(plain_password, hashed_password)


def createAccessToken(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt


def createRefreshToken(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt
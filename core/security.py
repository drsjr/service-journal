from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import Any, Union

from jose import JWTError, jwt
from passlib.context import CryptContext

from model.token_model import TokenData
from model.error_model import ApiError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "752b3f39e938f67f65de56f2500f5eadddc1443f04ccaa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 59

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

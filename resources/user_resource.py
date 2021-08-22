from fastapi import Depends, FastAPI, HTTPException, status
from datetime import timedelta

from repository.database import Database
from repository.user_repository import UserRepository
from model.error_model import ApiError
from model.user_model import User

import core.security as security


class UserResource():
    def __init__(self):
        self.repository = UserRepository(Database())

    def authenticate_user(self, email: str, password: str):
        user: User = self.repository.get_query_by_email(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ApiError(
                    code=status.HTTP_401_UNAUTHORIZED, 
                    message="email invalid", 
                    short="incorrect_credential").dict(),
                headers={"WWW-Authenticate": "Bearer"}
            )

        if security.verify_password(password, user.password) is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ApiError(
                    code=status.HTTP_401_UNAUTHORIZED, 
                    message="password invalid", 
                    short="incorrect_credential").dict(),
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_access = security.create_access_token(user.email, expires_delta=access_token_expires)

        return {"access_token": token_access, "token_type": "bearer"}

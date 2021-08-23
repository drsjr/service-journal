from model.model import TokenData
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


from datetime import timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer

from repository.database import Database
from repository.user_repository import UserRepository
from model.error_model import ApiError
from model.user_model import User, UserInfo
from model.token_model import TokenData

import core.security as security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserResource():
    def __init__(self):
        self.repository = UserRepository(Database())
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

    def get_user_into_by_email(self, email) -> UserInfo:
        user: UserInfo = self.repository.get_query_by_email(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ApiError(
                    code=status.HTTP_404_NOT_FOUND, 
                    message="User not found.", 
                    short="user_not_found").dict())
        
        return user


    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", oauth2_scheme)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ApiError(
                    code=status.HTTP_401_UNAUTHORIZED, 
                    message="invalide access", 
                    short="credential_expired").dict(),
            headers={"WWW-Authenticate": "Bearer"})

        token_data = None
        try:
            payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
                
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        print(token_data)
        user: User = self.repository.get_query_by_email(email=token_data.email)
        print(user)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ApiError(
                    code=status.HTTP_404_NOT_FOUND, 
                    message="User not found.", 
                    short="user_not_found").dict())
        return user
   
    #async def get_current_active_user(self, current_user: User = Depends(get_current_user)):
    #    if current_user.disabled:
    #        raise HTTPException(
    #            status_code=status.HTTP_400_BAD_REQUEST, 
    #            detail=ApiError(code=status.HTTP_400_BAD_REQUEST, message="User Inactive", short="user_inactive").dict())
    #    return current_user




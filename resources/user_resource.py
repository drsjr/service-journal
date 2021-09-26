from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer

from repository.database import Database
from repository.user_repository import UserRepository

from model.user_model import User, UserInfo
from model.token_model import TokenData, Token

from core import security
from core import handling_error as error

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserResource():

    def __init__(self):

        self.repository = UserRepository(Database())

    def authenticate_user(self, email: str, password: str) -> Token:
        user: User = self.repository.get_query_by_email(email=email)

        if not user:
            raise error.http_422_incorrect_email_or_password()

        if security.verify_password(password, user.password) is False:
            raise error.http_422_incorrect_email_or_password()
        
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_access = security.create_access_token(user.email, expires_delta=access_token_expires)

        return token_access

    def get_user_into_by_email(self, email) -> UserInfo:
        user: UserInfo = self.repository.get_query_by_email(email=email)

        if not user:
            raise error.http_404_object_not_found("User not found.", "user_not_found")
        
        return user


    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:

        token_data = None

        try:
            payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise error.http_401_expired_token_access()
                
            token_data = TokenData(email=email)
        except JWTError:
            raise error.http_401_expired_token_access()


        user: User = self.repository.get_query_by_email(email=token_data.email)

        if user is None:
            raise error.http_401_expired_token_access()
        return user


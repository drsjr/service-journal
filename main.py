
from model.error_model import ApiError
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from fastapi import Depends, FastAPI, HTTPException, status


from model.user_model import User, UserInfo
from model.token_model import Token
from resources.user_resource import UserResource


user_resource = UserResource()
app = FastAPI()

async def get_current_active_user(current_user: User = Depends(user_resource.get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=ApiError(code=status.HTTP_400_BAD_REQUEST, message="User Inactive", short="user_inactive").dict())
    return current_user

#####################################
#   Authentication Section          #
#####################################

@app.post("/token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return user_resource.authenticate_user(form_data.username, form_data.password)

@app.get("/users/me/", response_model=UserInfo)
async def user_info(current_user: User = Depends(get_current_active_user)):
    return UserInfo(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        updated_at=current_user.updated_at)



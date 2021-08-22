
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from model.token_model import Token
from resources.user_resource import UserResource


user_resource = UserResource()
app = FastAPI()

#####################################
#   Authentication Section          #
#####################################

@app.post("/token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return user_resource.authenticate_user(form_data.username, form_data.password)

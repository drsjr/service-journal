
from typing import List
from starlette import status
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from model.news_model import FrontPage, News
from model.error_model import ApiError
from model.user_model import User, UserInfo
from model.token_model import Token
from model.category_model import Category
from model.paragraph_model import Paragraph


from resources.article_resource import ArticleResource
from resources.user_resource import UserResource
from resources.category_resource import CategoryResource
from resources.front_page_resource import FrontPageResource


user_resource = UserResource()
category_resource = CategoryResource()
front_page_resource = FrontPageResource()
article_resource = ArticleResource()


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


#####################################
#   Category Section                #
#####################################

@app.get("/category", response_model=List[Category])
async def user_info(current_user: User = Depends(get_current_active_user)) -> List[Category]:
    return category_resource.get_all_categories()


@app.get("/category/{id}", response_model=Category)
async def user_info(id: int, current_user: User = Depends(get_current_active_user)):
    return category_resource.get_category_by_id(id)


#####################################
#   News Section                    #
#####################################

@app.get("/frontpage", response_model=FrontPage)
async def user_info(current_user: User = Depends(get_current_active_user)):
    return front_page_resource.get_front_page()

@app.get("/news/category/{category_id}", response_model=List[News])
async def user_info(category_id: int, current_user: User = Depends(get_current_active_user)):
    return front_page_resource.get_news_by_category(category_id)

#####################################
#   Article Section                 #
#####################################

@app.get("/article/{article_id}/paragraphs", response_model=List[Paragraph])
async def user_info(article_id: int, current_user: User = Depends(get_current_active_user)):
    return article_resource.get_paragraphs(article_id)
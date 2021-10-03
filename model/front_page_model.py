from typing import List, Optional
from pydantic import BaseModel


class FrontPage(BaseModel):
    id: int
    created_at: str

class NewsFromFrontPage(BaseModel):
    front_page_id: int
    article_id: int
    place: str

class FrontPageNews(FrontPage):
    news: Optional[List[NewsFromFrontPage]]
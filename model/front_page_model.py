from typing import List, Optional
from pydantic import BaseModel
from model.news_model import News

class FrontPage(BaseModel):
    main_main: News
    news_carrossel: List[News]
    news_column: List[News]

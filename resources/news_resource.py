from typing import List
from repository.database import Database
from model.news_model import News
from repository.news_repository import NewsRepository


class NewsResource():

    def __init__(self) -> None:
        self.repository = NewsRepository(Database())


    def get_news_by_category_id(self, category_id: int, offset: int, limit: int) -> List[News]:
            return self.repository.get_news_by_category(
                category_id=category_id, 
                offset=offset, 
                limit=limit
            )
    

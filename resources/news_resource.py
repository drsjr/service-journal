from typing import List
from repository.database import Database
from model.news_model import News
from repository.news_repository import NewsRepository

from core import handling_error as error

class NewsResource():

    def __init__(self) -> None:
        self.repository = NewsRepository(Database())


    def get_news_by_category_id(self, category_id: int, offset: int, limit: int) -> List[News]:
            return self.repository.get_news_by_category(
                category_id=category_id, 
                offset=offset, 
                limit=limit
            )
    def get_news_by_article_id(self, article_id: int) -> News:
            news = self.repository.get_news_by_id(article_id=article_id)
            if news is None:
                raise error.http_404_object_not_found("News not found!", "news_not_found")
            return news
    

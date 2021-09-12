from typing import List
from model.news_model import FrontPage, News
from repository.database import Database
from repository.news_repository import NewsRepository


class FrontPageResource():

    def __init__(self) -> None:
        self.repository = NewsRepository(Database())


    def get_front_page(self) -> FrontPage:
        return self.repository.get_last_front_page()

    def get_news_by_category(self, category_id: int) -> List[News]:
        return self.repository.get_news_by_category(category_id)

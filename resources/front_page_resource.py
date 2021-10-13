from repository.news_repository import NewsRepository
from typing import List
from model.front_page_model import FrontPage, FrontPageNews
from repository.front_page_repository import FrontPageRepository
from repository.database import Database


class FrontPageResource():

    def __init__(self) -> None:
        self.front_page = FrontPageRepository(Database())
        self.news_repo = NewsRepository(Database())


    def get_front_page_update(self) -> FrontPage:
        return self.front_page.get_front_page_update()


    def get_front_page(self) -> FrontPageNews:
        return self.front_page.get_front_page_with_article_id()


    def get_front_page_with_news(self) -> FrontPageNews:
        front_page = self.front_page.get_front_page_with_article_id()

        for i in front_page.news:
            i.news = self.news_repo.get_news_by_id(i.article_id)
        return front_page
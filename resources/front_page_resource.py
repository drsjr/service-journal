from typing import List
from model.front_page_model import FrontPage, FrontPageNews
from repository.front_page_repository import FrontPageRepository
from repository.database import Database


class FrontPageResource():

    def __init__(self) -> None:
        self.front_page = FrontPageRepository(Database())


    def get_front_page_update(self) -> FrontPage:
        return self.front_page.get_front_page_update()


    def get_front_page(self) -> FrontPageNews:
        return self.front_page.get_front_page_with_article_id()
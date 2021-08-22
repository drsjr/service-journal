from typing import List
from repository.database import Database

from starlette import responses
from model.front_page_model import FrontPage

class FrontPageRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()

    def get_front_page() -> FrontPage:
        pass

    

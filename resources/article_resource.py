from typing import List
from model.paragraph_model import Paragraph
from repository.database import Database
from repository.article_repository import ArticleRepository


class ArticleResource():

    def __init__(self) -> None:
        self.repository = ArticleRepository(Database())


    def get_paragraphs(self, article_id: int) -> List[Paragraph]:
        return self.repository.get_paragraph_by_article_id(article_id)

    

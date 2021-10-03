from typing import List
from repository.database import Database

from model.front_page_model import FrontPage, FrontPageNews, NewsFromFrontPage

QUERY_FRONT_PAGE = """
        SELECT 
            id, 
            created_at 
        FROM front_page
        ORDER BY id DESC
        LIMIT 1;
    """

QUERY_FRONT_PAGE_ARTICLE_ID = """
        SELECT front_page_id, article_id, place FROM (
            SELECT front_page_id, article_id, 'main' AS place FROM news_main
            UNION
            SELECT front_page_id, article_id, 'carrossel' AS place FROM news_carrossel 
            UNION
            SELECT front_page_id, article_id, 'column' AS place FROM news_column 
            UNION
            SELECT front_page_id, article_id, 'other' AS place FROM news_other) AS T
        WHERE T.front_page_id = %s
        ORDER BY place
"""

class FrontPageRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()

    def get_front_page_update(self) -> FrontPage:
        self.cursor.execute(QUERY_FRONT_PAGE, [])
        result = self.cursor.fetchone()

        front = FrontPage(
            id = result[0],
            created_at= str(result[1]))

        return front


    def get_front_page_with_article_id(self) -> FrontPageNews:
        self.cursor.execute(QUERY_FRONT_PAGE, [])
        result = self.cursor.fetchone()

        front = FrontPageNews(
                    id = result[0],
                    created_at = str(result[1]),
                    news = [])

        self.cursor.execute(QUERY_FRONT_PAGE_ARTICLE_ID, [front.id])
        result = self.cursor.fetchall()

        front.news = []

        for item in result:
            front.news.append(
                NewsFromFrontPage(
                    front_page_id = item[0],
                    article_id = item[1],
                    place = item[2]
                )
            )

        return front

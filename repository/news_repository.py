from repository.database import Database
from model.news_model import News

QUERY_NEWS_BY_ID = """
        SELECT
            a.id,
            a.url,
            a.title,
            a.subtitle,
            a.image,
            a.category_id,
            a.created_at
        FROM article a
        WHERE a.id = %s;
    """

QUERY_PAGINATION = """

        SELECT 
            n._id,
            n.created_at,
            n.news
        FROM news n
        WHERE n.category = {0}
        GROUP BY n._id, n.news->'url_path' 
        ORDER BY n._id DESC
        OFFSET {1} FETCH NEXT {2} ROW ONLY
    """

QUERY_NEWS_BY_CATEGORY = """
        SELECT 
            ar.id,
            ar.url,
            ar.title,
            ar.subtitle,
            ar.image,
            ar.category_id,
            ar.created_at
        FROM article ar
        INNER JOIN category ca ON ca.id = ar.category_id
        WHERE ar.category_id = %s
        ORDER BY id DESC
        OFFSET {1} FETCH NEXT {2} ROW ONLY
    """


class NewsRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()

    def get_news_by_id(self, id: int) -> News:
        self.cursor.execute(QUERY_NEWS_BY_ID, [id])
        result = self.cursor.fetchone()

        if result is None:
            return None

        return News(id=result[0], 
                url=result[1], 
                title=result[2], 
                subtitle=result[3], 
                image=result[4], 
                category=result[5], 
                created_at=result[6])  

    
    def get_news_by_category(self, category_id: int):
        self.cursor.execute(QUERY_NEWS_BY_CATEGORY, [category_id])
        result = self.cursor.fetchall()

        news_by_category = []

        for news in result:
            news_by_category.append(
                News(id=news[0], 
                    url=news[1], 
                    title=news[2], 
                    subtitle=news[3], 
                    image=news[4], 
                    category=news[5], 
                    created_at=str(news[6])
                )
            )
        return news_by_category

            

         
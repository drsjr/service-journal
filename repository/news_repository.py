from repository.database import Database
from model.news_model import News, FrontPage


FRONT_TYPES = [
    ("main", "news_main"), 
    ("carrossel", "news_carrossel"), 
    ("column", "news_column"), 
    ("other", "news_other")]

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

QUERY_FRONT_PAGE = """
        SELECT 
            id, 
            created_at 
        FROM front_page
        ORDER BY id DESC
        LIMIT 1;
    """

QUERY_PAGINATION = """
        SELECT 
            n._id,
            n.created_at,
            n.news
        FROM news n
        WHERE n.category = %s
        GROUP BY n._id, n.news->'url_path' 
        ORDER BY n._id DESC
        OFFSET %s FETCH NEXT %s ROW ONLY
    """

QUERY_FRONT_PAGE_TABLES = """
            SELECT
                '{0}' AS is_from,
                ar.id,
                ar.url,
                ar.title,
                ar.subtitle,
                ar.image,
                ar.category_id,
                ar.created_at,
                fp.id AS front_page_id
            FROM front_page fp
            INNER JOIN {1} n ON n.front_page_id = fp.id
            INNER JOIN article ar ON n.article_id = ar.id
            WHERE n.front_page_id = {2};
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
        LIMIT 10;
    """


class NewsRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()

    def get_news_by_id(self, id: int) -> FrontPage:
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
    
    def get_last_front_page(self) -> FrontPage:
        self.cursor.execute(QUERY_FRONT_PAGE, [])
        result = self.cursor.fetchone()

        if result is None:
            return None

        front_page = FrontPage(
            id=result[0],
            carrossel=[],
            column=[],
            other=[],
            created_at=str(result[1])) 

        front_page.main = self.query_front_by_type(FRONT_TYPES[0][0], FRONT_TYPES[0][1], front_page.id)[0]
        front_page.carrossel = self.query_front_by_type(FRONT_TYPES[1][0], FRONT_TYPES[1][1], front_page.id)
        front_page.column = self.query_front_by_type(FRONT_TYPES[2][0], FRONT_TYPES[2][1], front_page.id)
        front_page.other = self.query_front_by_type(FRONT_TYPES[3][0], FRONT_TYPES[3][1], front_page.id)

        return front_page

    def query_front_by_type(self, column: str, table: str, front_page_id):
        response = []
        query = QUERY_FRONT_PAGE_TABLES.format(column, table, front_page_id)
        self.cursor.execute(query, [])
        result = self.cursor.fetchall()

        for news in result:
            response.append(
                News(id=news[1], 
                    url=news[2], 
                    title=news[3], 
                    subtitle=news[4], 
                    image=news[5], 
                    category=news[6], 
                    created_at=str(news[7])
                    )
            )

        return response
            

         
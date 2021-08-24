from repository.database import Database
from model.news_model import News, FrontPage

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

QUERY_CANSADA = """
        SELECT 
            t.is_from,
            t.id,
            t.url,
            t.title,
            t.subtitle,
            t.image,
            t.category_id,
            t.created_at,
            t.front_page_id
        FROM (
            SELECT
                'main' AS is_from,
                ar.id,
                ar.url,
                ar.title,
                ar.subtitle,
                ar.image,
                ar.category_id,
                ar.created_at,
                fp.id AS front_page_id
            FROM front_page fp
            INNER JOIN news_main n ON n.front_page_id = fp.id
            INNER JOIN article ar ON n.article_id = ar.id
            UNION
            SELECT 
                'carrossel' AS is_from,
                ar.id,
                ar.url,
                ar.title,
                ar.subtitle,
                ar.image,
                ar.category_id,
                ar.created_at,
                fp.id AS front_page_id
            FROM front_page fp
            INNER JOIN news_carrossel n ON n.front_page_id = fp.id
            INNER JOIN article ar ON n.article_id = ar.id
            UNION
            SELECT 
                'column' AS is_from,
                ar.id,
                ar.url,
                ar.title,
                ar.subtitle,
                ar.image,
                ar.category_id,
                ar.created_at,
                fp.id AS front_page_id
            FROM front_page fp
            INNER JOIN news_column n ON n.front_page_id = fp.id
            INNER JOIN article ar ON n.article_id = ar.id) AS t
        WHERE t.front_page_id = %s;
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

    
    def get_last_front_page(self) -> FrontPage:
        self.cursor.execute(QUERY_FRONT_PAGE, [])
        result = self.cursor.fetchone()

        if result is None:
            return None

        front_page = FrontPage(
            id=result[0],
            carrossel=[],
            column=[],
            created_at=str(result[1])) 

        self.cursor.execute(QUERY_CANSADA, [front_page.id])
        result = self.cursor.fetchall()

        for news in result:

            if news[0] == 'main':
                front_page.main = News(id=news[1], 
                                            url=news[2], 
                                            title=news[3], 
                                            subtitle=news[4], 
                                            image=news[5], 
                                            category=news[6], 
                                            created_at=str(news[7]))

            elif news[0] == 'carrossel':
                front_page.carrossel.append(News(id=news[1], 
                                            url=news[2], 
                                            title=news[3], 
                                            subtitle=news[4], 
                                            image=news[5], 
                                            category=news[6], 
                                            created_at=str(news[7])))
            else:
                front_page.column.append(News(id=news[1], 
                                            url=news[2], 
                                            title=news[3], 
                                            subtitle=news[4], 
                                            image=news[5], 
                                            category=news[6], 
                                            created_at=str(news[7])))
            
        return front_page

        
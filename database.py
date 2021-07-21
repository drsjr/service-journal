
from typing import List

from starlette import responses
from model import News, User, Category, FrontPage
import psycopg2

class Database():

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.connection = psycopg2.connect(
            host='192.168.15.35',
            user='folha',
            password='folha',
            dbname='folha',
            port=5432)


class UserRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()
    
    def get_query_by_username(self, username: str) -> User:
        self.cursor.execute("SELECT username, password, full_name, disabled FROM users where username = %s", [username])
        obj = self.cursor.fetchone()
        if obj is None:
            return None
        user = User(username=obj[0], password=obj[1], full_name=obj[2], disabled=False)
        return user


class NewsRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()


    def get_query_category_pagination(self, category: str, offset: int = 0, limit: int = 5):
        response = []
        query = """
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
        self.cursor.execute(query, [category, offset, limit])
        result = self.cursor.fetchall()
        for obj in result:
            print(obj[0],"\n", 
                obj[2]["url_path"],"\n", 
                obj[2]["url_image"],"\n", 
                obj[2]["news_title"],"\n", 
                obj[2]["news_subtitle"],"\n", 
                obj[2]["news_time"],"\n", 
                category,"\n", "\n---------------------------------------------------------------------------------------------------")
            response.append(
                News(id=obj[0], 
                    url_path=obj[2]["url_path"], 
                    url_image=(obj[2]["url_image"] if obj[2]["url_image"] is not None else ""), 
                    title=obj[2]["news_title"], 
                    subtitle=obj[2]["news_subtitle"], 
                    time=obj[2]["news_time"], 
                    category=category)
                )

        return response

class CategoryRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()


    def get_all_categories(self):
        response = []
        query = """
            SELECT 
                _id,
                "name",
                path,
                code,
                is_enable
            FROM category
        """
        self.cursor.execute(query, [])

        result = self.cursor.fetchall()
        for obj in result:
            print(obj[0], 
                    obj[1], 
                    obj[2], 
                    obj[3],
                    obj[4], "\n---------------------------------------------------------------------------------------------------")

            response.append(
                Category(
                    id=obj[0], 
                    name=obj[1], 
                    path=obj[2], 
                    code=obj[3],
                    is_enable=obj[4])
                )

        return response


class FrontPageRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()


    def get_last_front_page(self):
        query = """
            SELECT 
                * 
            FROM principal 
            ORDER BY _id DESC LIMIT 1
        """
        self.cursor.execute(query, [])
        result = self.cursor.fetchone()[2]
        
        main = News(id=0, 
                        url_path=result['main_news']["link"], 
                        title=result['main_news']["title"], 
                        subtitle=result['main_news']["subtitle"], 
                        url_image="", 
                        time="", 
                        category="")

        carrossel = []
        for o in result['carrossel']:
            carrossel.append(Carrossel(id=0,
                url_path=o['link'], 
                title="", 
                subtitle=o['subtitle'], 
                url_image=o['image_linke'], 
                time="", 
                category=""))

        column = []
        for o in result['column_news']:
            column.append(News(id=0, 
                url_path=o['link'], 
                title=o['link'], 
                subtitle=o['subtitle'], 
                url_image="", 
                time="", 
                category=""))

        response = FrontPage(main=main, carrossel=carrossel, column=column)
        return response
        

    




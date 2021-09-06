import psycopg2
import os

class Database():

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('DT_HOST'),
            user=os.getenv('DT_USER'),
            password=os.getenv('DT_PASS'),
            dbname=os.getenv('DT_NAME'),
            port=os.getenv('DT_PORT'))

#class NewsRepository():
#
#    def __init__(self, db: Database):
#        self.cursor = db.connection.cursor()
#
#
#    def get_query_category_pagination(self, category: str, offset: int = 0, limit: int = 5):
#        response = []
#        query = """
#            SELECT 
#                n._id,
#                n.created_at,
#                n.news
#            FROM news n
#            WHERE n.category = %s
#            GROUP BY n._id, n.news->'url_path' 
#            ORDER BY n._id DESC
#            OFFSET %s FETCH NEXT %s ROW ONLY
#        """
#        self.cursor.execute(query, [category, offset, limit])
#        result = self.cursor.fetchall()
#        for obj in result:
#            print(obj[0],"\n", 
#                obj[2]["url_path"],"\n", 
#                obj[2]["url_image"],"\n", 
#                obj[2]["news_title"],"\n", 
#                obj[2]["news_subtitle"],"\n", 
#                obj[2]["news_time"],"\n", 
#                category,"\n", "\n---------------------------------------------------------------------------------------------------")
#            response.append(
#                News(id=obj[0], 
#                    url_path=obj[2]["url_path"], 
#                    url_image=(obj[2]["url_image"] if obj[2]["url_image"] is not None else ""), 
#                    title=obj[2]["news_title"], 
#                    subtitle=obj[2]["news_subtitle"], 
#                    time=obj[2]["news_time"], 
#                    category=category)
#                )
#
#        return response


#class FrontPageRepository():
#
#    def __init__(self, db: Database):
#        self.cursor = db.connection.cursor()
#
#
#    def get_last_front_page(self):
#        query = """
#            SELECT 
#                * 
#            FROM principal 
#            ORDER BY _id DESC LIMIT 1
#        """
#        self.cursor.execute(query, [])
#        result = self.cursor.fetchone()[2]
#        
#        main = News(id=0, 
#                        url_path=result['main_news']["link"], 
#                        title=result['main_news']["title"], 
#                        subtitle=result['main_news']["subtitle"], 
#                        url_image="", 
#                        time="", 
#                        category="")
#
#        carrossel = []
#        for o in result['carrossel']:
#            carrossel.append(News(id=0,
#                url_path=o['link'], 
#                title="", 
#                subtitle=o['subtitle'], 
#                url_image=o['image_linke'], 
#                time="", 
#                category=""))
#
#        column = []
#        for o in result['column_news']:
#            column.append(News(id=0, 
#                url_path=o['link'], 
#                title=o['link'], 
#                subtitle=o['subtitle'], 
#                url_image="", 
#                time="", 
#                category=""))
#
#        response = FrontPage(main=main, carrossel=carrossel, column=column)
#        return response
        

    




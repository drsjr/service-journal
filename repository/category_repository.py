from repository.database import Database
from model.category_model import Category


QUERY_ALL_CATEGORIES =  """
            SELECT 
                id,
                "name",
                path,
                code,
                "disabled"
            FROM category
        """

QUERY_CATEGORY_BY_ID =  """
            SELECT 
                id,
                "name",
                path,
                code,
                "disabled"
            FROM category
            WHERE id = %s
        """


class CategoryRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()


    def get_all_categories(self):
        response = []
        self.cursor.execute(QUERY_ALL_CATEGORIES, [])

        result = self.cursor.fetchall()
        for obj in result:
            response.append(
                Category(
                    id=obj[0], 
                    name=obj[1], 
                    path=obj[2], 
                    code=obj[3],
                    disabled=obj[4])
                )

        return response

    def get_category_by_id(self, id: int):

        self.cursor.execute(QUERY_CATEGORY_BY_ID, [id])
        result = self.cursor.fetchone()
        
        if result is None:
            return None

        return Category(
                id=result[0], 
                name=result[1], 
                path=result[2], 
                code=result[3],
                disabled=result[4])
            
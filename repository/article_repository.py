from repository.database import Database
from model.paragraph_model import Paragraph


QUERY_PARAGRAPHS_BY_ARTICLE_ID = """
    SELECT 
        p.id,
        p.paragraph, 
        p.article_id,
        p."order"
    FROM paragraph p
    WHERE p.article_id = %s
    ORDER BY p."order"
    """

class ArticleRepository():

    def __init__(self, db: Database):
        self.cursor = db.connection.cursor()


    def get_paragraph_by_article_id(self, article_id: int):
        response = []
        self.cursor.execute(QUERY_PARAGRAPHS_BY_ARTICLE_ID, [article_id])

        result = self.cursor.fetchall()
        for obj in result:
            response.append(
                Paragraph(
                    id=obj[0], 
                    paragraph=obj[1], 
                    article_id=obj[2], 
                    order=obj[3]
                    )
                )

        return response
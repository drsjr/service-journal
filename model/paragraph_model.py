from pydantic import BaseModel


class Paragraph(BaseModel):
    id: int
    paragraph: str
    order: int
    article_id: int

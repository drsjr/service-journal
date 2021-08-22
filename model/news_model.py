from pydantic import BaseModel

class News(BaseModel):
    id: int
    url: str
    created_at: str
    title: str
    subtitle: str
    iamge: str
    category: int

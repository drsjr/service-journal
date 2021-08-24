from typing import List, Optional
from pydantic import BaseModel


class News(BaseModel):
    id: int
    url_path: str
    url_image: str
    title: str
    subtitle: str
    time: str
    category: str

class Category(BaseModel):
    id: int
    name: str
    path: str
    code: int
    is_enable: bool

class FrontPage(BaseModel):
    main: News
    carrossel: List[News]
    column: List[News]


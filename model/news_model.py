from typing import List, Optional
from pydantic import BaseModel

class News(BaseModel):
    id: int
    url: str
    created_at: str
    title: str
    subtitle: str
    image: str
    category: int

class FrontPage(BaseModel):
    id: int
    main: Optional[News]
    carrossel: Optional[List[News]]
    column: Optional[List[News]]
    created_at: str

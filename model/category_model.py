from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    path: str
    code: int
    disabled: bool


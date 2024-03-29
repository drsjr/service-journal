from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    password: str
    full_name: str
    created_at: str
    updated_at: str
    disabled: bool

class UserInfo(BaseModel):
    id: int
    email: str
    full_name: str
    updated_at: str

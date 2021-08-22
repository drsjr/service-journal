from pydantic.main import BaseModel

class ApiError(BaseModel):
    code: int
    message: str
    short: str

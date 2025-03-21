from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    name: str
    author: str


class BookSchemaCreate(BaseModel):
    name: str
    author: str

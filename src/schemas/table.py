from pydantic import BaseModel


class TableAdd(BaseModel):
    name: str
    seats: int
    location: str


class Table(TableAdd):
    id: int
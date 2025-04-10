from src.models.table import TablesORM
from src.schemas.table import Table
from src.CRUD.base import BaseCRUD


class TablesCRUD(BaseCRUD):
    model = TablesORM
    schema = Table
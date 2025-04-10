from src.exceptions import (
    KeyIsStillReferencedException,
    ObjectNotFoundException,
    TableKeyIsStillReferencedException,
    TableNotFoundException,
)
from src.services.base import BaseService
from src.schemas.table import Table, TableAdd


class TablesService(BaseService):
    async def create_table(self, table_data: TableAdd) -> Table:
        new_table = await self.db.tables.create(data=table_data)
        await self.db.commit()
        return new_table

    async def get_tables(self) -> list[Table]:
        try:
            return await self.db.tables.get_all()
        except ObjectNotFoundException:
            raise TableNotFoundException

    async def delete_table(self, table_id: int) -> Table:
        try:
            deleted_table = await self.db.tables.delete(id=table_id)
        except KeyIsStillReferencedException:
            raise TableKeyIsStillReferencedException
        except ObjectNotFoundException:
            raise TableNotFoundException
        await self.db.commit()
        return deleted_table

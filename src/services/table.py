from src.services.base import BaseService
from src.schemas.table import Table, TableAdd


class TablesService(BaseService):
    async def create_table(self, table_data: TableAdd) -> Table:
        new_table = await self.db.tables.create(data=table_data)
        await self.db.commit()
        return new_table
    
    async def get_tables(self) -> list[Table]:
        return await self.db.tables.get_all()
    
    async def delete_table(self, table_id: int) -> Table:
        deleted_table = await self.db.tables.delete(id=table_id)
        await self.db.commit()
        return deleted_table
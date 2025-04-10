from fastapi import APIRouter, Body

from src.services.table import TablesService
from src.routers.dependencies import DBDep
from src.schemas.table import TableAdd


router = APIRouter(prefix="/tables", tags=["Столики"])


@router.post("")
async def add_table(db: DBDep, table_data: TableAdd = Body()):
    new_table = await TablesService(db).create_table(table_data=table_data)
    return {"status": "OK", "data": new_table}


@router.get("")
async def get_tables(db: DBDep):
    tables = await TablesService(db).get_tables()
    return {"status": "OK", "data": tables}


@router.delete("/{id}")
async def delete_table(db: DBDep, id: int):
    deleted_table = await TablesService(db).delete_table(table_id=id)
    return {"status": "OK", "data": deleted_table}
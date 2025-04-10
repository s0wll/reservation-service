from fastapi import APIRouter, Body

from src.exceptions import (
    TableKeyIsStillReferencedException,
    TableKeyIsStillReferencedHTTPException,
    TableNotFoundException,
    TableNotFoundHTTPException,
)
from src.logger import logger
from src.services.table import TablesService
from src.routers.dependencies import DBDep
from src.schemas.table import TableAdd


router = APIRouter(prefix="/tables", tags=["Столики"])


@router.post("")
async def add_table(db: DBDep, table_data: TableAdd = Body()):
    logger.info("Добавление столика /add_table")
    new_table = await TablesService(db).create_table(table_data=table_data)
    logger.info("Успешное добавление столика")
    return {"status": "OK", "data": new_table}


@router.get("")
async def get_tables(db: DBDep):
    try:
        logger.info("Получение списка столиков /get_tables")
        tables = await TablesService(db).get_tables()
        logger.info("Успешное получение списка столиков")
    except TableNotFoundException:
        logger.error("Ошибка получения столиков: данные не найдены")
        raise TableNotFoundHTTPException
    return {"status": "OK", "data": tables}


@router.delete("/{id}")
async def delete_table(db: DBDep, id: int):
    try:
        logger.info("Удаление столика /delete_table")
        deleted_table = await TablesService(db).delete_table(table_id=id)
        logger.info("Успешное удаление столика")
    except TableKeyIsStillReferencedException:
        logger.error("Ошибка удаления столика: ключ еще используется в другой таблице")
        raise TableKeyIsStillReferencedHTTPException
    except TableNotFoundException:
        raise TableNotFoundHTTPException
    return {"status": "OK", "data": deleted_table}
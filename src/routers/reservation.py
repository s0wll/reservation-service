from fastapi import APIRouter, Body

from src.exceptions import (
    ReservationAlreadyExistsException,
    ReservationNotFoundException,
    ReservationNotFoundHTTPException,
    TableNotFoundException,
    TableNotFoundHTTPException,
    ReservationAlreadyExistsHTTPException,
)
from src.logger import logger
from src.services.reservation import ReservationsService
from src.routers.dependencies import DBDep
from src.schemas.reservation import ReservationAdd


router = APIRouter(prefix="/reservations", tags=["Бронирования"])


@router.post("")
async def add_reservation(db: DBDep, reservation_data: ReservationAdd = Body(
        openapi_examples={
            "1": {
                "value": {
                    "customer_name": "Mark",
                    "table_id": 1,
                    "reservation_time": "2025-04-10T18:00",
                    "duration_minutes": 120
                }
            },
            "2": {
                "value": {
                    "customer_name": "Oleg",
                    "table_id": 2,
                    "reservation_time": "2025-04-10T12:30",
                    "duration_minutes": 60
                }
            }
        }
    )
):
    try:
        logger.info("Добавление бронирования столика /add_reservation")
        new_reservation = await ReservationsService(db).create_reservation(
            reservation_data=reservation_data
        )
        logger.info("Успешное добавление бронирования")
    except TableNotFoundException:
        logger.error("Ошибка добавления бронирования: столик не найден")
        raise TableNotFoundHTTPException
    except ReservationAlreadyExistsException:
        logger.error("Ошибка добавления бронирования: на данное время уже есть бронь")
        raise ReservationAlreadyExistsHTTPException
    return {"status": "OK", "data": new_reservation}


@router.get("")
async def get_reservations(db: DBDep):
    try:
        logger.info("Получение списка бронирований /get_reservations")
        reservations = await ReservationsService(db).get_reservations()
        logger.info("Успешное получение списка бронирований")
    except ReservationNotFoundException:
        logger.error("Ошибка получения списка бронирований: бронь не найдена")
        raise ReservationNotFoundHTTPException
    return {"status": "OK", "data": reservations}


@router.delete("/{id}")
async def delete_reservation(db: DBDep, id: int):
    try:
        logger.info("Удаление бронирования /delete_reservation")
        deleted_reservation = await ReservationsService(db).delete_reservation(reservation_id=id)
        logger.info("Успешное удаление бронирования")
    except ReservationNotFoundException:
        logger.error("Ошибка удаления бронирования: бронь не найдена")
        raise ReservationNotFoundHTTPException
    return {"status": "OK", "data": deleted_reservation}
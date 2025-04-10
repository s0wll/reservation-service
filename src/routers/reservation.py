from fastapi import APIRouter, Body

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
    new_reservation = await ReservationsService(db).create_reservation(
        reservation_data=reservation_data
    )
    return {"status": "OK", "data": new_reservation}


@router.get("")
async def get_reservations(db: DBDep):
    reservations = await ReservationsService(db).get_reservations()
    return {"status": "OK", "data": reservations}


@router.delete("/{id}")
async def delete_reservation(db: DBDep, id: int):
    deleted_reservation = await ReservationsService(db).delete_reservation(reservation_id=id)
    return {"status": "OK", "data": deleted_reservation}
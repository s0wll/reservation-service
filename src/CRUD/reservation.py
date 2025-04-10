from src.models.reservation import ReservationsORM
from src.schemas.reservation import Reservation
from src.CRUD.base import BaseCRUD


class ReservationsCRUD(BaseCRUD):
    model = ReservationsORM
    schema = Reservation
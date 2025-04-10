from datetime import datetime

from pydantic import BaseModel


class ReservationAdd(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int


class Reservation(ReservationAdd):
    id: int
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import Base


class ReservationsORM(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]
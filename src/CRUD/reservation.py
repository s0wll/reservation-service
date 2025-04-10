from datetime import timedelta

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import ForeignKeyViolationError


from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.models.reservation import ReservationsORM
from src.schemas.reservation import Reservation, ReservationAdd
from src.CRUD.base import BaseCRUD


class ReservationsCRUD(BaseCRUD):
    model = ReservationsORM
    schema = Reservation

    # Отдельный метод для операции добавления бронирования в БД
    async def create_reservation(self, reservation_data: ReservationAdd) -> Reservation:
        # Определяем временной интервал нового бронирования
        new_reserv_start = reservation_data.reservation_time
        new_reserv_end = new_reserv_start + timedelta(minutes=reservation_data.duration_minutes)

        # Получаем все существующие бронирования для этого столика
        table_reservs_query = select(self.model).where(
            self.model.table_id == reservation_data.table_id
        )
        result = await self.session.execute(table_reservs_query)
        existing_reservations = result.scalars().all()

        # Проверяем каждое существующее бронирование на пересечение по времени с новым
        for reservation in existing_reservations:
            existing_start = reservation.reservation_time
            existing_end = existing_start + timedelta(minutes=reservation.duration_minutes)
            
            if (new_reserv_start < existing_end) and (new_reserv_end > existing_start):
                raise ObjectAlreadyExistsException

        # Добавление бронирования, если нет пересечений по времени с уже существующими
        new_reservation = insert(self.model).values(**reservation_data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(new_reservation)
        except IntegrityError as exc:
            if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                raise ObjectNotFoundException from exc
            else:
                raise exc
        return self.schema.model_validate(result.scalars().one(), from_attributes=True)

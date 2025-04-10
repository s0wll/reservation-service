from src.services.base import BaseService
from src.schemas.reservation import Reservation, ReservationAdd


class ReservationsService(BaseService):
    async def create_reservation(self, reservation_data: ReservationAdd) -> Reservation:
        new_reservation = await self.db.reservations.create_reservation(reservation_data=reservation_data)
        await self.db.commit()
        return new_reservation
    
    async def get_reservations(self) -> list[Reservation]:
        return await self.db.reservations.get_all()
    
    async def delete_reservation(self, reservation_id: int) -> Reservation:
        deleted_reservation = await self.db.reservations.delete(id=reservation_id)
        await self.db.commit()
        return deleted_reservation
    

# Это пример внедрения паттерна проектирования services.
# Если бы была нужда в доп функционале для работы с бронированиями или столиками (пр.: доп проверки, 
# relationships, пагинация, фильтрация и тп), 
# то это все можно было бы реализовать здесь, нагрузив функции, а в /routers каждя ф-я остается лаконичной и 
# ненагруженной большим кол-вом кода.

from pydantic import BaseModel
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import ForeignKeyViolationError

from src.exceptions import KeyIsStillReferencedException, ObjectNotFoundException
from src.logger import logger

class BaseCRUD:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    # Метод для добавления данных в БД
    async def create(self, data: BaseModel) -> BaseModel:
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        # Валидация (приведение результата к pydantic модели) и возврат добавленной модели
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model
    
    # Метод для получения всех данных из БД
    async def get_all(self) -> list[BaseModel]:
        query = select(self.model)
        result = await self.session.execute(query)
        models = [
            self.schema.model_validate(one, from_attributes=True)
            for one in result.scalars().all()
        ]
        if not models:
            logger.error("Ошибка получения данных из БД, данные не найдены")
            raise ObjectNotFoundException
        return models
    
    # Здесь мог бы быть метод для изменения данных в БД (можно расширить функционал сервиса)

    # Метод для удаления данных из БД по фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        try:
            result = await self.session.execute(delete_stmt)
        except IntegrityError as exc:
            #logger error(тип)
            if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                logger.error(f"Ошибка удаления данных из БД, тип ошибки: {type(exc.orig.__cause__)=}")
                raise KeyIsStillReferencedException from exc
            else:
                logger.error(
                    f"Незнакомая ошибка, не удалось удалить данные из БД, тип ошибки: {type(exc.orig.__cause__)=}"
                )
                raise exc
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model
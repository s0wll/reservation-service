from pydantic import BaseModel
from sqlalchemy import delete, insert, select


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
        return models
    
    # Здесь мог бы быть метод для изменения данных в БД (можно расширить функционал сервиса)

    # Метод для удаления данных из БД по фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        delete_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(delete_stmt)
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model
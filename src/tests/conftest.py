import json

import pytest
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel

from src.main import app
from src.database import Base, engine
from src.config import settings
from src.database import async_session_maker
from src.utils.db_manager import DBManager
from src.schemas.reservation import ReservationAdd
from src.schemas.table import TableAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode() -> None:
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "reservation-service-test"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def create_test_data(setup_database):
    async def load_and_validate_data(file_path: str, schema: BaseModel) -> list[BaseModel]:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
            return [schema.model_validate(item) for item in data]
    
    tables = await load_and_validate_data("src/tests/test_data/mock_tables.json", TableAdd)
    reservations = await load_and_validate_data("src/tests/test_data/mock_reservations.json", ReservationAdd)

    async with DBManager(session_factory=async_session_maker) as db:
        for table in tables:
            await db.tables.create(table)
        for reservation in reservations:
            await db.reservations.create(reservation)
        await db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
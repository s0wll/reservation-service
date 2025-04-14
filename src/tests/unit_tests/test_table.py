from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_add_table(ac: AsyncClient):
    response = await ac.post(
        "/tables", json={"name": "test_table", "seats": 2, "location": "test_location"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["data"]["name"] == "test_table"
    assert result["data"]["seats"] == 2
    assert result["data"]["location"] == "test_location"


@pytest.mark.asyncio
async def test_get_tables(ac: AsyncClient):
    response = await ac.get("/tables")
    assert response.status_code == 200
    assert response.json()["data"]


@pytest.mark.asyncio
async def test_delete_table(ac: AsyncClient):
    response = await ac.delete("/tables/3")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 3

@pytest.mark.asyncio
async def test_delete_table_with_reservations(ac: AsyncClient):
    # Сначала создаем столик
    await ac.post(
        "/tables",
        json={"name": "Table for delete", "seats": 4, "location": "Near window"}
    )

    # Создаем бронь для этого столика
    await ac.post(
        "/reservations",
        json={
            "customer_name": "test_customer",
            "table_id": 1,
            "reservation_time": "2025-10-10T18:00",
            "duration_minutes": 120,
        }
    )

    # Пытаемся удалить столик с активной броней
    response = await ac.delete("/tables/1")
    assert response.status_code == 409
    assert "Ключ стола все еще используется в другой таблице" in response.json()["detail"]

@pytest.mark.asyncio
async def test_invalid_table_data(ac: AsyncClient):
    # Пытаемся создать столик с некорректными данными
    response = await ac.post(
        "/tables",
        json={"name": 5, "seats": "InvInp", "location": 10}  # Все поля невалидны
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(e["loc"] == ["body", "name"] for e in errors)
    assert any(e["loc"] == ["body", "seats"] for e in errors)
    assert any(e["loc"] == ["body", "location"] for e in errors)

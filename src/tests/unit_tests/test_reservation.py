from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_add_reservation(ac: AsyncClient):
    response = await ac.post(
        "/reservations",
        json={
            "customer_name": "test_customer",
            "table_id": 4,
            "reservation_time": "2025-10-10T18:00",
            "duration_minutes": 120,
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert result["data"]["customer_name"] == "test_customer"
    assert result["data"]["table_id"] == 4
    assert result["data"]["reservation_time"] == "2025-10-10T18:00:00"
    assert result["data"]["duration_minutes"] == 120

@pytest.mark.asyncio
async def test_get_reservations(ac: AsyncClient):
    response = await ac.get("/reservations")
    assert response.status_code == 200
    assert response.json()["data"]

@pytest.mark.asyncio
async def test_delete_reservation(ac: AsyncClient):
    response = await ac.delete("/reservations/1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1

@pytest.mark.asyncio
async def test_conflict_reservation(ac: AsyncClient):
    # Сначала создаем резервирование
    await ac.post(
        "/reservations",
        json={
            "customer_name": "customer1",
            "table_id": 1,
            "reservation_time": "2025-10-10T18:00",
            "duration_minutes": 120,
        },
    )

    # Пытаемся создать конфликтующее резервирование
    response = await ac.post(
        "/reservations",
        json={
            "customer_name": "customer2",
            "table_id": 1,
            "reservation_time": "2025-10-10T19:00",
            "duration_minutes": 30,
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Стол уже забронирован на данное время"

@pytest.mark.asyncio
async def test_invalid_reservation_data(ac: AsyncClient):
    # Пытаемся создать резервирование с некорректными данными
    response = await ac.post(
        "/reservations",
        json={
            "customer_name": "",
            "table_id": 1,
            "reservation_time": "2025-10-10T18:00",
            "duration_minutes": 120,
        },
    )
    assert response.status_code == 409

    # Попытка создать бронь с нулевой длительностью
    response = await ac.post(
        "/reservations",
        json={
            "customer_name": "edge_case_customer",
            "table_id": 3,
            "reservation_time": "2025-10-10T20:00",
            "duration_minutes": 0,
        },
    )
    assert response.status_code == 409

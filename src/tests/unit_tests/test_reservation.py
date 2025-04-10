from httpx import AsyncClient


async def test_add_reservation(ac: AsyncClient):
    response = await ac.post(
        "/reservations",
        json={
            "customer_name": "test_customer",
            "table_id": 4,
            "reservation_time": "2025-10-10T18:00",
            "duration_minutes": 120
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert result["data"]["customer_name"] == "test_customer"
    assert result["data"]["table_id"] == 4
    assert result["data"]["reservation_time"] == "2025-10-10T18:00:00"
    assert result["data"]["duration_minutes"] == 120

async def test_get_reservations(ac: AsyncClient):
    response = await ac.get("/reservations")
    assert response.status_code == 200
    assert response.json()["data"]

async def test_delete_reservation(ac: AsyncClient):
    response = await ac.delete("/reservations/1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
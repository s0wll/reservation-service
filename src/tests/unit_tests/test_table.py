from httpx import AsyncClient


async def test_add_table(ac: AsyncClient):
    response = await ac.post(
        "/tables",
        json={
            "name": "test_table",
            "seats": 2,
            "location": "test_location"
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert result["data"]["name"] == "test_table"
    assert result["data"]["seats"] == 2
    assert result["data"]["location"] == "test_location"

async def test_get_tables(ac: AsyncClient):
    response = await ac.get("/tables")
    assert response.status_code == 200
    assert response.json()["data"]

async def test_delete_table(ac: AsyncClient):
    response = await ac.delete("/tables/3")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 3
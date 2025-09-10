import uuid
import pytest


@pytest.mark.anyio
async def test_create_and_get_item(client):
    title = f"Test Item {uuid.uuid4()}"
    
    # Create item
    resp = await client.post("/items/", json={"title": title, "description": "Test description"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == title
    item_id = data["id"]
    
    # Get item
    resp = await client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == item_id
    
    # List items
    resp = await client.get("/items/", params={"title": title})
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert any(item["id"] == item_id for item in items)

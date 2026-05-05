import pytest 

async def test_create_short_url(async_client):
    response = await async_client.post("/url", json={"url": "https://www.google.com"})
    assert response.status_code == 201
    assert "short_url" in response.json()
    assert response.json()["short_url"] is not None
    
async def test_repeat_post(async_client):
    response1 = await async_client.post("/url", json={"url": "https://www.google.com"})
    response2 = await async_client.post("/url", json={"url": "https://www.google.com"})
    assert response1.json()["short_url"] == response2.json()["short_url"]
    
async def test_post_invalid_url(async_client):
    response = await async_client.post("/url", json={'url': "hello"})
    assert response.status_code == 422
    
async def test_get_invalid_short_code(async_client):
    short_code = "hello"
    response = await async_client.get(url=f"/{short_code}")
    assert response.status_code == 404
    

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_hello_world():
    """Test the hello world endpoint"""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_hello_name():
    """Test the personalized greeting endpoint"""
    name = "Alice"
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}

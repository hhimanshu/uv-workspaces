from fastapi.testclient import TestClient
from src._lib.endpoints import ApiEndpoints
from src.main import app
from src.test_utils.api_path import get_api_path


client = TestClient(app)


def test_hello_world():
    """Test the hello world endpoint"""
    response = client.get(get_api_path(ApiEndpoints.API.HELLO.path))
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_hello_name():
    """Test the personalized greeting endpoint"""
    name = "Alice"
    response = client.get(get_api_path(f"{ApiEndpoints.API.HELLO.path}/{name}"))
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}!"}

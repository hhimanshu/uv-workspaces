from fastapi.testclient import TestClient
from src._lib.shared import ApiVersion
from src.main import app
from src.test_utils.api_path import get_api_path


client = TestClient(app)


def test_create_user_success():
    """Test successful user creation with valid data"""
    user_data = {
        "name": "testuser2",
        "email": "test2@example.com",
    }
    response = client.post(
        get_api_path("/users"),
        json=user_data,
    )
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["created_at"] is not None
    assert data["updated_at"] is None


def test_create_user_preview_version():
    """Test user creation with preview version"""
    user_data = {
        "name": "testuser3",
        "email": "testuser3@example.com",
    }

    response = client.post(
        get_api_path("/users"),
        json=user_data,
        headers={"api-version": ApiVersion.V2024_10_PREVIEW},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["created_at"] is not None
    assert data["updated_at"] is None


def test_create_user_invalid_email():
    """Test user creation with invalid email format"""
    user_data = {
        "name": "testuser4",
        "email": "invalidemail",
    }
    response = client.post(
        get_api_path("/users"),
        json=user_data,
    )
    assert response.status_code == 422
    data = response.json()
    assert "email" in str(data["detail"]).lower()


def test_create_user_missing_required():
    """Test user creation with missing required fields"""
    user_data = {
        "name": "testuser5",
    }
    response = client.post(
        get_api_path("/users"),
        json=user_data,
    )
    assert response.status_code == 422
    data = response.json()
    assert "email" in str(data["detail"]).lower()


def test_create_user_empty_values():
    """Test user creation with empty string values"""
    user_data = {
        "name": "",
        "email": "",
    }
    response = client.post(
        get_api_path("/users"),
        json=user_data,
    )
    assert response.status_code == 422
    data = response.json()
    assert "name" in str(data["detail"]).lower()
    assert "email" in str(data["detail"]).lower()


def test_create_user_invalid_json():
    """Test user creation with invalid JSON payload"""
    response = client.post(
        get_api_path("/users"),
        content="invalid json",
    )
    assert response.status_code == 422
    data = response.json()
    assert "json" in str(data["detail"]).lower()

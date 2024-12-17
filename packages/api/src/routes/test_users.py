import pytest
from fastapi.testclient import TestClient
from services.dependencies import get_user_service
from src._lib.endpoints import ApiEndpoints
from src._lib.shared import ApiVersion
from src.main import app
from src.test_utils.api_path import get_api_path
from src.test_utils.test_dependencies import TestDependencies


@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_user_service] = TestDependencies.get_user_service
    yield
    app.dependency_overrides = {}
    TestDependencies.cleanup()


client = TestClient(app)


def test_create_user_success():
    """Test successful user creation with valid data"""
    user_data = {
        "name": "testuser2",
        "email": "test2@example.com",
    }
    response = client.post(
        get_api_path(ApiEndpoints.API.USERS.path),
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
        get_api_path(ApiEndpoints.API.USERS.path),
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
        get_api_path(ApiEndpoints.API.USERS.path),
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
        get_api_path(ApiEndpoints.API.USERS.path),
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
        get_api_path(ApiEndpoints.API.USERS.path),
        json=user_data,
    )
    assert response.status_code == 422
    data = response.json()
    assert "name" in str(data["detail"]).lower()
    assert "email" in str(data["detail"]).lower()


def test_create_user_invalid_json():
    """Test user creation with invalid JSON payload"""
    response = client.post(
        get_api_path(ApiEndpoints.API.USERS.path),
        content="invalid json",
    )
    assert response.status_code == 422
    data = response.json()
    assert "json" in str(data["detail"]).lower()

# src/services/test_user_service.py
from datetime import datetime
from unittest.mock import create_autospec

import pytest
from faker import Faker
from typeid import TypeID

from ..dto.user_dto import CreateUserRequest, UpdateUserRequest
from ..models.user import User
from ..repositories.base_repository import BaseRepository
from .user_service import UserService

fake = Faker()


class TestUserService:
    @pytest.fixture
    def mock_repository(self):
        return create_autospec(BaseRepository, instance=True)

    @pytest.fixture
    def user_service(self, mock_repository):
        return UserService(mock_repository)

    def test_to_response(self, user_service):
        user = User(
            id=TypeID(prefix="user"),
            name=fake.name(),
            email=fake.email(),
            created_at=datetime.now(),
        )
        response = user_service._to_response(user)
        assert str(response.id).startswith("user_")
        assert response.name == user.name
        assert response.email == user.email

    @pytest.mark.asyncio
    async def test_create_user(self, user_service, mock_repository):
        request = CreateUserRequest(name=fake.name(), email=fake.email())

        mock_repository.create.return_value = User(
            id=TypeID(prefix="user"), name=request.name, email=request.email
        )

        response = await user_service.create_user(request)
        assert str(response.id).startswith("user_")
        assert response.name == request.name
        assert response.email == request.email
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user(self, user_service, mock_repository):
        user_id = TypeID(prefix="user")
        update_request = UpdateUserRequest(name=fake.name())

        mock_repository.update.return_value = User(
            id=user_id, name=update_request.name, email=fake.email()
        )

        response = await user_service.update_user(user_id, update_request)
        assert response.name == update_request.name
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_by_email(self, user_service, mock_repository):
        email = fake.email()
        user = User(id=TypeID(prefix="user"), name=fake.name(), email=email)
        mock_repository.find_one.return_value = user

        response = await user_service.find_by_email(email)
        assert str(response.id).startswith("user_")
        assert response.email == email
        mock_repository.find_one.assert_called_once_with({"email": email})

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_service, mock_repository):
        user_id = TypeID(prefix="user")
        update_request = UpdateUserRequest(name=fake.name())
        mock_repository.update.return_value = None

        response = await user_service.update_user(user_id, update_request)
        assert response is None
        mock_repository.update.assert_called_once()

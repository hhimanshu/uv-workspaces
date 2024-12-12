from bson import ObjectId
import pytest
from datetime import UTC, datetime
from ...models.user import User
from .main import UserManagement


class TestUserManagement:
    @pytest.fixture
    async def user_management(self):
        manager = UserManagement()
        await manager.collection.delete_many({})
        return manager

    @pytest.mark.asyncio
    async def test_create_user_success(self, user_management):
        manager = await user_management

        user = User(
            email="test@example.com", name="Test User", created_at=datetime.now(UTC)
        )

        created_user = await manager.create_user(user)
        assert created_user.id is not None

        # Use ObjectId for lookup
        db_user = await manager.collection.find_one({"_id": ObjectId(created_user.id)})
        assert db_user is not None

    @pytest.mark.asyncio
    async def test_get_existing_user(self, user_management):
        manager = await user_management

        user = User(
            email="test@example.com", name="Test User", created_at=datetime.now(UTC)
        )
        created_user = await manager.create_user(user)
        retrieved_user = await manager.get_user(created_user.id)
        assert retrieved_user is not None
        assert retrieved_user.email == user.email
        assert retrieved_user.name == user.name

    @pytest.mark.asyncio
    async def test_get_nonexistent_user(self, user_management):
        manager = await user_management
        retrieved_user = await manager.get_user("nonexistent_id")
        assert retrieved_user is None
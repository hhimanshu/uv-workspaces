import pytest
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from testcontainers.mongodb import MongoDbContainer

from ..models.user import User
from ..shared.database import get_database_settings
from .user_repo import UserRepository


class TestUserRepository:
    @pytest.fixture(scope="session")
    def mongodb_container(self):
        with MongoDbContainer() as mongo:
            yield mongo

    @pytest.fixture
    async def user_repository(self, mongodb_container):
        mongodb_url = mongodb_container.get_connection_url()
        db_settings = get_database_settings(mongodb_url=mongodb_url, db_name="test_db")
        await db_settings.initialize()

        repo = UserRepository(db_settings=db_settings)
        await repo.initialize()
        yield repo
        await repo.collection.delete_many({})
        await repo.close()
        await db_settings.close()

    @pytest.fixture
    def user_data(self):
        return {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "addresses": [
                {
                    "street": "123 Test St",
                    "city": "Test City",
                    "state": "TS",
                    "postal_code": "12345",
                }
            ],
            "phones": [
                {"number": "+11234567890", "type": "mobile", "is_primary": True}
            ],
        }

    @pytest.mark.asyncio
    async def test_create_user(self, user_repository, user_data):
        user = User(**user_data)
        created_user = await user_repository.create(user)

        assert created_user.id is not None
        assert created_user.email == user_data["email"]

        # Verify in database
        db_user = await user_repository.collection.find_one(
            {"_id": ObjectId(created_user.id)}
        )
        assert db_user is not None
        assert db_user["email"] == user_data["email"]

    @pytest.mark.asyncio
    async def test_find_by_id(self, user_repository, user_data):
        user = User(**user_data)
        created_user = await user_repository.create(user)

        found_user = await user_repository.find_by_id(created_user.id)
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == user_data["email"]

    @pytest.mark.asyncio
    async def test_find_by_email(self, user_repository, user_data):
        user = User(**user_data)
        await user_repository.create(user)

        found_user = await user_repository.find_by_email(user_data["email"])
        assert found_user is not None
        assert found_user.email == user_data["email"]

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository, user_data):
        user = User(**user_data)
        created_user = await user_repository.create(user)

        created_user.first_name = "Updated"
        updated_user = await user_repository.update(created_user.id, created_user)

        assert updated_user is not None
        assert updated_user.first_name == "Updated"

        # Verify in database
        db_user = await user_repository.collection.find_one(
            {"_id": ObjectId(created_user.id)}
        )
        assert db_user["first_name"] == "Updated"

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository, user_data):
        user = User(**user_data)
        created_user = await user_repository.create(user)

        result = await user_repository.delete(created_user.id)
        assert result is True

        # Verify deletion
        db_user = await user_repository.collection.find_one(
            {"_id": ObjectId(created_user.id)}
        )
        assert db_user is None

    @pytest.mark.asyncio
    async def test_find_active_users(self, user_repository, user_data):
        # Create active user
        active_user = User(**user_data)
        await user_repository.create(active_user)

        # Create inactive user
        inactive_data = user_data.copy()
        inactive_data["email"] = "inactive@example.com"
        inactive_data["is_active"] = False
        inactive_user = User(**inactive_data)
        await user_repository.create(inactive_user)

        active_users = await user_repository.find_active_users()
        assert len(active_users) == 1
        assert active_users[0].email == active_user.email

    @pytest.mark.asyncio
    async def test_unique_email_constraint(self, user_repository, user_data):
        user1 = User(**user_data)
        await user_repository.create(user1)

        # Try to create another user with same email
        user2 = User(**user_data)
        with pytest.raises(DuplicateKeyError):  # MongoDB will raise duplicate key error
            await user_repository.create(user2)

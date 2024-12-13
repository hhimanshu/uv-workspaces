import logging

import pytest
from faker import Faker
from testcontainers.mongodb import MongoDbContainer
from typeid import TypeID

from ..models.user import User
from .user_repo import UserRepository

fake = Faker()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestUserRepository:
    @pytest.fixture(scope="session")
    def mongodb_container(self):
        logger.info("Starting MongoDB test container")
        with MongoDbContainer() as mongo:
            yield mongo

    @pytest.fixture
    async def user_repository(self, mongodb_container):
        mongodb_url = mongodb_container.get_connection_url()
        repo = UserRepository(mongodb_url=mongodb_url, db_name="test_db")
        await repo.collection.delete_many({})
        return repo

    @pytest.mark.asyncio
    async def test_create_and_get_user(self, user_repository):
        user = User(name=fake.name(), email=fake.email())
        created_user = await user_repository.create_user(user)

        assert created_user.id is not None
        created_id_as_str = str(created_user.id)
        assert created_id_as_str.startswith("user")

        retrieved_user = await user_repository.get_by_id(created_user.id)
        assert retrieved_user is not None

        retrieved_id_as_str = str(retrieved_user.id)
        assert retrieved_id_as_str == created_id_as_str
        assert retrieved_user.email == user.email

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, user_repository):
        user = User(name=fake.name(), email=fake.email())
        await user_repository.create_user(user)

        with pytest.raises(ValueError, match="already exists"):
            await user_repository.create_user(user)

    @pytest.mark.asyncio
    async def test_find_users_by_name(self, user_repository):
        user1 = User(name="John Doe", email=fake.email())
        user2 = User(name="John Smith", email=fake.email())
        await user_repository.create_user(user1)
        await user_repository.create_user(user2)

        users = await user_repository.find_users_by_name("John")
        assert len(users) == 2
        assert all(user.name.startswith("John") for user in users)

    @pytest.mark.asyncio
    async def test_update_email(self, user_repository):
        user = User(name=fake.name(), email=fake.email())
        created_user = await user_repository.create_user(user)
        new_email = fake.email()

        updated_user = await user_repository.update_email(created_user.id, new_email)
        assert updated_user is not None
        assert updated_user.email == new_email
        assert updated_user.updated_at is not None

    @pytest.mark.asyncio
    async def test_nonexistent_user(self, user_repository):
        random_id = TypeID()
        user = await user_repository.get_by_id(random_id)
        assert user is None

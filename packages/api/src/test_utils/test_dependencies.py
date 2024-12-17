from repositories.user_repo import UserRepository
from services.user_service import UserService
from testcontainers.mongodb import MongoDbContainer


class TestDependencies:
    _container = None
    _user_service = None

    @classmethod
    def get_container(cls):
        if not cls._container:
            cls._container = MongoDbContainer()
            cls._container.start()
        return cls._container

    @classmethod
    def get_user_service(cls) -> UserService:
        if not cls._user_service:
            mongodb_url = cls.get_container().get_connection_url()
            repository = UserRepository(mongodb_url=mongodb_url, db_name="test_db")
            cls._user_service = UserService(repository)
        return cls._user_service

    @classmethod
    def cleanup(cls):
        if cls._container:
            cls._container.stop()
            cls._container = None
        cls._user_service = None

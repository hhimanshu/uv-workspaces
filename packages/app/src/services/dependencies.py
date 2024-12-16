from config import get_app_db_name, get_mongodb_url
from repositories.user_repo import UserRepository
from services.user_service import UserService


async def get_user_service() -> UserService:
    # Create and return UserService instance
    mongodb_url = get_mongodb_url()
    db_name = get_app_db_name()
    repository = UserRepository(mongodb_url=mongodb_url, db_name=db_name)
    return UserService(repository)

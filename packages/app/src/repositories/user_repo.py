# src/repositories/user_repository.py
from datetime import UTC, datetime
from typing import List, Optional

from typeid import TypeID

from models.user import User

from .base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, mongodb_url: str, db_name: str):
        super().__init__(mongodb_url, db_name, User)

    async def find_by_email(self, email: str) -> Optional[User]:
        return await self.find_one({"email": email})

    async def find_users_by_name(self, name: str) -> List[User]:
        return await self.find_many({"name": {"$regex": name, "$options": "i"}})

    async def update_email(self, id: TypeID, new_email: str) -> Optional[User]:
        return await self.update(
            id, {"email": new_email, "updated_at": datetime.now(UTC)}
        )

    async def create_user(self, user: User) -> User:
        existing_user = await self.find_by_email(user.email)
        if existing_user:
            raise ValueError(f"User with email {user.email} already exists")
        user.id = TypeID(prefix="user")
        return await self.create(user)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.find_one({"email": email})

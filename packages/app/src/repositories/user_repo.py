from typing import List, Optional

from shared.database import DatabaseSettings

from ..models.user import User
from .base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db_settings: Optional[DatabaseSettings] = None):
        super().__init__(User, db_settings)

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self.collection.find_one({"email": email})
        return User.model_validate(result) if result else None

    async def find_active_users(self) -> List[User]:
        cursor = self.collection.find({"is_active": True})
        documents = await cursor.to_list(length=None)
        return [User.model_validate(doc) for doc in documents]

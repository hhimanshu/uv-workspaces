from typing import List, Optional

from ..models.user import User
from .base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        """Initialize UserRepository with User model class."""
        super().__init__(User)

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by their email address."""
        result = await self.collection.find_one({"email": email})
        return User.model_validate(result) if result else None

    async def find_active_users(self) -> List[User]:
        """Find all active users."""
        cursor = self.collection.find({"is_active": True})
        documents = await cursor.to_list(length=None)
        return [User.model_validate(doc) for doc in documents]

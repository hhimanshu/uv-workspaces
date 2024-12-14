# src/services/user_service.py
from datetime import UTC, datetime
from typing import Optional

from typeid import TypeID

from ..dto.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse
from ..models.user import User
from ..repositories.base_repository import BaseRepository
from .base_service import BaseService


class UserService(BaseService[User, UserResponse]):
    def __init__(self, repository: BaseRepository[User]):
        super().__init__(repository)

    def _to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def create_user(self, user_request: CreateUserRequest) -> UserResponse:
        user = User(
            id=TypeID(prefix="user"), name=user_request.name, email=user_request.email
        )
        created_user = await self.repository.create(user)
        return self._to_response(created_user)

    async def update_user(
        self, id: TypeID, update_request: UpdateUserRequest
    ) -> Optional[UserResponse]:
        update_dict = update_request.model_dump(exclude_unset=True)
        if update_dict:
            update_dict["updated_at"] = datetime.now(UTC)
            user = await self.repository.update(id, update_dict)
            return self._to_response(user) if user else None
        return await self.get_by_id(id)

    async def find_by_email(self, email: str) -> Optional[UserResponse]:
        user = await self.repository.find_one({"email": email})
        return self._to_response(user) if user else None

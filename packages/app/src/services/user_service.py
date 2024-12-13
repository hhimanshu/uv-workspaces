# app/src/capabilities/user_management/services/user_service.py
from typing import List

from ..exceptions.user_errors import DuplicateEmailError, UserNotFoundError
from ..models.user import AUser
from ..repositories.user_repo import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    async def create_user(self, user: AUser) -> AUser:
        # Check if email already exists
        existing_user = await self._repository.find_by_email(user.email)
        if existing_user:
            raise DuplicateEmailError(f"User with email {user.email} already exists")

        return await self._repository.create(user)

    async def get_user(self, user_id: str) -> AUser:
        user = await self._repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user

    async def get_users(self) -> List[AUser]:
        return await self._repository.find_all()

    async def update_user(self, user_id: str, user_update: AUser) -> AUser:
        # Check if user exists
        existing_user = await self.get_user(user_id)

        # If email is being changed, check for duplicates
        if user_update.email != existing_user.email:
            email_user = await self._repository.find_by_email(user_update.email)
            if email_user:
                raise DuplicateEmailError(
                    f"User with email {user_update.email} already exists"
                )

        updated_user = await self._repository.update(user_id, user_update)
        if not updated_user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return updated_user

    async def delete_user(self, user_id: str) -> bool:
        # Check if user exists
        await self.get_user(user_id)
        return await self._repository.delete(user_id)

    async def get_active_users(self) -> List[AUser]:
        return await self._repository.find_active_users()

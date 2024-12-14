# src/services/base_service.py
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from typeid import TypeID

from ..models.base_model import BaseDocument
from ..repositories.base_repository import BaseRepository

T = TypeVar("T", bound=BaseDocument)
R = TypeVar("R", bound=BaseModel)


class BaseService(Generic[T, R]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    def _to_response(self, model: T) -> R:
        raise NotImplementedError

    async def get_by_id(self, id: TypeID) -> Optional[R]:
        model = await self.repository.get_by_id(id)
        return self._to_response(model) if model else None

    async def delete(self, id: TypeID) -> bool:
        return await self.repository.delete(id)

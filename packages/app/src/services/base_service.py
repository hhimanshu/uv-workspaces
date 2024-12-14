from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from typeid import TypeID

from ..models.base_model import BaseDocument
from ..repositories.base_repository import BaseRepository

D = TypeVar("D", bound=BaseDocument)
R = TypeVar("R", bound=BaseModel)  # R represents the response model


class BaseService(Generic[D, R]):
    def __init__(self, repository: BaseRepository[D]):
        self.repository = repository

    def _to_response(self, doc: D) -> R:
        raise NotImplementedError

    async def get_by_id(self, id: TypeID) -> Optional[R]:
        doc = await self.repository.get_by_id(id)
        return self._to_response(doc) if doc else None

    async def delete(self, id: TypeID) -> bool:
        return await self.repository.delete(id)

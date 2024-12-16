from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from typeid import TypeID

from models.base_model import BaseDocument
from repositories.base_repository import BaseRepository

Doc = TypeVar("Doc", bound=BaseDocument)
Res = TypeVar("Res", bound=BaseModel)
Repo = TypeVar("RepoType", bound=BaseRepository[Doc])


class BaseService(Generic[Doc, Repo, Res]):
    def __init__(self, repository: Repo):
        self.repository = repository

    def _to_response(self, doc: Doc) -> Res:
        raise NotImplementedError

    async def get_by_id(self, id: TypeID) -> Optional[Res]:
        doc = await self.repository.get_by_id(id)
        return self._to_response(doc) if doc else None

    async def delete(self, id: TypeID) -> bool:
        return await self.repository.delete(id)

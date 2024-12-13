from datetime import UTC, datetime
from typing import Optional
from typeid import TypeID

from pydantic import BaseModel, Field


class BaseDocument(BaseModel):
    id: TypeID = Field(default_factory=TypeID)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    @classmethod
    def get_collection_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_indexes(cls) -> list:
        return []

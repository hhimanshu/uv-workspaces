from datetime import UTC, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseDocument(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: Optional[datetime] = None

    @classmethod
    def get_collection_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_indexes(cls) -> list:
        return []

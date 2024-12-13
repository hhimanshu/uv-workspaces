from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseDocument(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

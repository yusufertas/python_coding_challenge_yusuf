from datetime import datetime
from time import strftime
from typing import Optional

from pydantic import BaseModel, validator


class AbstractEntity(BaseModel):
    id: Optional[int]


class TodoEntry(AbstractEntity):
    summary: str
    detail: Optional[str]
    tag: Optional[str]
    created_at: datetime
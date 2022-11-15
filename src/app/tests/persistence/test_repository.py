import json
from datetime import datetime, timezone

import asyncio_redis
import pytest

from entities import TodoEntry
from persistence.errors import EntityNotFoundError, CreateError
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository


@pytest.mark.asyncio
async def test_get_todo_entry() -> None:
    r = await asyncio_redis.Connection.create(host='localhost', port=6379)
    entity = await r.get("1")
    entity = TodoEntry(**json.loads(entity))
    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_not_found_error() -> None:
    r = await asyncio_redis.Connection.create(host='localhost', port=6379)
    with pytest.raises(TypeError):
        entity = await r.get("42")
        await entity


@pytest.mark.asyncio
async def test_save_todo_entry() -> None:
    data = TodoEntry(
        id=2,
        summary="Buy flowers to my wife",
        detail="We have marriage anniversary",
        created_at=datetime.now(tz=timezone.utc),
    )
    r = await asyncio_redis.Connection.create(host='localhost', port=6379)

    await r.set(str(data.id), json.dumps(data.dict(), default=str))
    entity = data
    assert isinstance(entity, TodoEntry)
    assert entity.id > 1


@pytest.mark.asyncio
async def test_todo_entry_create_error() -> None:
    data = TodoEntry(
        summary="Lorem Ipsum",
        detail=None,
        created_at=datetime.now(tz=timezone.utc),
    )
    r = await asyncio_redis.Connection.create(host='localhost', port=6379)
    with pytest.raises(TypeError):
       await TodoEntry(**data)
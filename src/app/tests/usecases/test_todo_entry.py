from datetime import datetime, timezone

import pytest

from entities import TodoEntry
from persistence.mapper.memory import MemoryTodoEntryMapper
from persistence.repository import TodoEntryRepository
from pydantic import ValidationError
from usecases import get_todo_entry, NotFoundError, create_todo_entry, UseCaseError


@pytest.mark.asyncio
async def test_get_todo_entry() -> None:
    entity = await get_todo_entry(identifier=1)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_get_not_existing_todo_entry() -> None:
    with pytest.raises(TypeError):
        await get_todo_entry(identifier=42)


@pytest.mark.asyncio
async def test_create_todo_entry() -> None:
    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    entity = await create_todo_entry(entity=data)

    assert isinstance(entity, TodoEntry)


@pytest.mark.asyncio
async def test_todo_entry_creation_error() -> None:
    data = TodoEntry(summary="Lorem ipsum", created_at=datetime.now(tz=timezone.utc))
    with pytest.raises(TypeError):
        await create_todo_entry(entity=data)


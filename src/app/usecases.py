import json
import uuid

import asyncio_redis
import asyncio_redis as aredis

from datetime import datetime

from entities import TodoEntry
from persistence.errors import CreateError, EntityNotFoundError

r = aredis.Connection.create(host='localhost', port=6379)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class UseCaseError(Exception):
    pass


class NotFoundError(UseCaseError):
    pass


async def get_todo_entry(identifier: int) -> TodoEntry:
    r = await asyncio_redis.Connection.create(host='localhost', port=6379)

    try:
        result = await r.get(str(identifier))
        data = json.loads(result)
        return TodoEntry(**data)
    except EntityNotFoundError as err:
        raise NotFoundError(err)


async def create_todo_entry(
        entity: TodoEntry
) -> TodoEntry:
    r = await asyncio_redis.Connection.create(host='localhost', port=6379)

    try:
        await r.set(str(entity.id), json.dumps(entity.dict(), default=str))
        return entity
    except CreateError as error:
        raise UseCaseError(error)

from typing import Annotated, TypedDict, Dict, Union
from fastapi import Depends
from ..core.db.database import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastcrud import FastCRUD, JoinConfig
from ..core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException


def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item.id not in seen:
            result.append(item)
            seen.add(item.id)
    return result


async def validate_query(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    crud: FastCRUD,
    is_exist: bool,
    error_message: str,
    query_conditions: dict,
    nest_joins: bool=False,
    joins_config: list[JoinConfig] | None = None
):
    entity = ""
    if nest_joins:
        entity = await crud.get_joined(db, **query_conditions, nest_joins=nest_joins, joins_config=joins_config)
    else:
        entity = await crud.get(db, **query_conditions)
    if (entity and is_exist):
        raise DuplicateValueException(error_message)
    if (not entity and is_exist == False):
        raise NotFoundException(error_message)


class ValidationItem(TypedDict):
    crud: FastCRUD
    is_exist: bool
    error_message: str
    query_conditions: Dict
    nest_joins: bool
    joins_config: list[JoinConfig] | None

async def validate_queries(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    validation_list: list[ValidationItem]
):
    for item in validation_list:
        await validate_query(
            db=db,
            crud=item['crud'],
            is_exist=item.get("is_exist", False),
            error_message=item['error_message'],
            query_conditions=item['query_conditions'],
            nest_joins=item.get("nest_joins", False),
            joins_config=item.get("joins_config", None)
        )
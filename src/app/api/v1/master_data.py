from typing import Annotated, Any


from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_user
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.db.database import async_get_db
from ...models.master_data import MasterData

from ...crud.crud_master_data import crud_master_data
from ...crud.crud_master_data_types import crud_master_data_types

from ...schemas.master_data import (
    MasterDataCreate,
    MasterDataCreateInternal,
    MasterDataRead,
    MasterDataUpdate,
    MasterDataUpdateInternal,
)
from ...schemas.user import UserRead

db_dependency = Annotated[AsyncSession, Depends(async_get_db)]
current_user_dependency = Annotated[UserRead, Depends(get_current_user)]

router = APIRouter(tags=["master_data"])


@router.post("/master-data", response_model=MasterDataRead, status_code=201)
async def write_role(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    master_data: MasterDataCreate
):
    name_exists = await crud_master_data.exists(db, name=master_data.name, is_deleted=False)
    if (name_exists):
        raise DuplicateValueException("Master data name already exists")
    
    code_exists = await crud_master_data_types.exists(db, code=master_data.code, is_deleted=False)
    if not code_exists:
        raise DuplicateValueException("Master data type code not found")
    
    master_data_internal_dict = master_data.model_dump()
    master_data_internal_dict["created_by"] = current_user["id"]
    master_data_internal_dict["updated_by"] = current_user["id"]
    master_data_internal_dict = MasterDataCreateInternal(**master_data_internal_dict)

    created_master_data = await crud_master_data.create(db, object=master_data_internal_dict)
    return created_master_data


@router.get("/master-data", response_model=PaginatedListResponse[MasterDataRead])
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    page: int = 1, items_per_page: int = 10
):
    master_data = await crud_master_data.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=MasterDataRead,
        is_deleted=False,
    )

    response = paginated_response(crud_data=master_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/master-data/{id}", response_model=MasterDataRead)
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
):
    master_data = await crud_master_data.get(db=db, id=id, is_deleted=False)
    if not master_data:
        raise NotFoundException("Master data not found")
    return master_data


@router.patch("/master-data/{id}")
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
    values: MasterDataUpdate
):
    master_data_exists = await crud_master_data.exists(db=db, id=id, is_deleted=False)
    if not master_data_exists:
        raise NotFoundException("Master data not found")

    master_data_internal_dict = values.model_dump(exclude_unset=True)
    master_data_internal_dict["updated_by"] = current_user["id"]

    
    await crud_master_data.update(db=db, object=MasterDataUpdateInternal(**master_data_internal_dict), id=id)

    return {"status": "success"}


@router.delete("/master-data/{id}")
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
):
    master_data_exists = await crud_master_data.exists(db=db, id=id, is_deleted=False)
    if not master_data_exists:
        raise NotFoundException("Master data not found")

    await crud_master_data.delete(db=db, id=id,is_deleted=False)

    return {"status": "success"}
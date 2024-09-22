from typing import Annotated, Any


from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession


from ...api.dependencies import get_current_user
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.db.database import async_get_db
from ...models.master_data_type import MasterDataType
from ...crud.crud_master_data_types import crud_master_data_types
from ...schemas.master_data_type import (
    MasterDataTypeCreate,
    MasterDataTypeCreateInternal,
    MasterDataTypeRead,
    MasterDataTypeUpdate,
    MasterDataTypeUpdateInternal,
)
from ...schemas.user import UserRead

db_dependency = Annotated[AsyncSession, Depends(async_get_db)]
current_user_dependency = Annotated[UserRead, Depends(get_current_user)]

router = APIRouter(tags=["master_data_types"])


@router.post("/master-data-type", response_model=MasterDataTypeRead, status_code=201)
async def write_role(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    master_data_type: MasterDataTypeCreate
):
    name_exists = await crud_master_data_types.exists(db, name=master_data_type.name, is_deleted=False)
    if (name_exists):
        raise DuplicateValueException("Master data type name already exists")
    
    code_exists = await crud_master_data_types.exists(db, code=master_data_type.code, is_deleted=False)
    if (code_exists):
        raise DuplicateValueException("Master data type code already exists")
    
    master_data_type_internal_dict = master_data_type.model_dump()
    master_data_type_internal_dict["created_by"] = current_user["id"]
    master_data_type_internal_dict["updated_by"] = current_user["id"]
    master_data_type_internal_dict = MasterDataTypeCreateInternal(**master_data_type_internal_dict)

    created_master_data_type = await crud_master_data_types.create(db, object=master_data_type_internal_dict)
    return created_master_data_type



@router.get("/master-data-types", response_model=PaginatedListResponse[MasterDataTypeRead])
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    page: int = 1, items_per_page: int = 10
):
    master_data_types = await crud_master_data_types.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=MasterDataTypeRead,
        is_deleted=False,
    )

    response = paginated_response(crud_data=master_data_types, page=page, items_per_page=items_per_page)
    return response


@router.get("/master-data-types/{id}", response_model=MasterDataTypeRead)
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
):
    master_data_type = await crud_master_data_types.get(db=db, id=id, is_deleted=False)
    if not master_data_type:
        raise NotFoundException("Master data type not found")
    return master_data_type


@router.patch("/master-data-types/{id}")
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
    values: MasterDataTypeUpdate
):
    master_data_type_exists = await crud_master_data_types.exists(db=db, id=id, is_deleted=False)
    if not master_data_type_exists:
        raise NotFoundException("Master data type not found")

    master_data_type_internal_dict = values.model_dump(exclude_unset=True)
    master_data_type_internal_dict["updated_by"] = current_user["id"]

    
    await crud_master_data_types.update(db=db, object=MasterDataTypeUpdateInternal(**master_data_type_internal_dict), id=id)

    return {"status": "success"}


@router.delete("/master-data-types/{id}")
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
):
    master_data_type_exists = await crud_master_data_types.exists(db=db, id=id, is_deleted=False)
    if not master_data_type_exists:
        raise NotFoundException("Master data type not found")

    await crud_master_data_types.delete(db=db, id=id,is_deleted=False)

    return {"status": "success"}

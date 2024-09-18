from typing import Annotated, Any


from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession


from ...api.dependencies import get_current_user
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.db.database import async_get_db
from ...models.role import Role
from ...crud.crud_roles import crud_roles
from ...schemas.role import (
    RoleCreate, 
    RoleCreateInternal, 
    RoleRead, RoleUpdate, 
    RoleUpdateInternal, 
    RoleDelete
)
from ...schemas.user import UserRead

db_dependency = Annotated[AsyncSession, Depends(async_get_db)]
current_user_dependency = Annotated[UserRead, Depends(get_current_user)]

router = APIRouter(tags=["roles"])


@router.post("/role", response_model=RoleRead, status_code=201)
async def write_role(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    role: RoleCreate
):
    is_exists = await crud_roles.exists(db, name=role.name, is_deleted=False)
    if (is_exists):
        raise DuplicateValueException("Role already exists")
    
    role_internal_dict = role.model_dump()
    role_internal_dict = RoleCreateInternal(**role_internal_dict)
    role_internal_dict["created_by"] = current_user["id"]
    role_internal_dict["updated_by"] = current_user["id"]

    created_role = await crud_roles.create(db, role_internal_dict)
    return created_role


@router.get("/roles", response_model=PaginatedListResponse[RoleRead])
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    page: int = 1, items_per_page: int = 10
):
    roles = await crud_roles.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=UserRead,
        is_deleted=False,
    )

    response = paginated_response(crud_data=roles, page=page, items_per_page=items_per_page)
    return response


@router.get("/roles/{id}", response_model=RoleRead)
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
    page: int = 1, item_per_pages: int = 10,
):
    role = await crud_roles.get(db=db, id=id, is_deleted=False)
    if not role:
        raise NotFoundException("Role not found")
    return role


@router.patch("/roles/{id}")
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
    values: RoleUpdate
):
    role_exists = await crud_roles.exists(db=db, id=id, is_deleted=False)
    if not role_exists:
        raise NotFoundException("Role not found")

    role_internal_dict = values.model_dump(exclude_unset=True)
    role_internal_dict["updated_by"] = current_user["id"]

    
    await crud_roles.update(db=db, object=RoleUpdateInternal(**role_internal_dict), id=id)

    return {"status": "success"}


@router.delete("/roles/{id}")
async def read_roles(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int,
):
    role_exists = await crud_roles.exists(db=db, id=id, is_deleted=False)
    if not role_exists:
        raise NotFoundException("Role not found")

    await crud_roles.delete(db=db, id=id,is_deleted=False)

    return {"status": "success"}

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from fastcrud import JoinConfig, aliased

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
from ...api.dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...core.helper import remove_duplicates
from ...crud.crud_users import crud_users
from ...crud.crud_roles import crud_roles
from ...crud.crud_user_role import crud_user_role
from ...schemas.user import UserCreate, UserCreateInternal, UserRead, UserUpdate, UserUpdateInternal, UserReadSub
from ...schemas.user_role import UserRoleCreateInternal, UserRoleRead
from ...schemas.role import RoleRead

from ...models.user import User, UserRole
from ...models.role import Role



router = APIRouter(tags=["users"])
db_dependency = Annotated[AsyncSession, Depends(async_get_db)]
current_user_dependency = Annotated[UserRead, Depends(get_current_user)]

@router.post("/user", status_code=201)
async def write_user(
    request: Request, user: UserCreate, current_user: current_user_dependency, db: db_dependency
) -> UserReadSub:
    # Query validate
    email_row = await crud_users.exists(db=db, email=user.email)
    if email_row:
        raise DuplicateValueException("Email is already registered")

    username_row = await crud_users.exists(db=db, username=user.username)
    if username_row:
        raise DuplicateValueException("Username not available")
    
    roles = await crud_roles.get_multi(db=db, id__in=user.roles, is_deleted=False)
    if len(user.roles) > len(roles["data"]):
        raise NotFoundException("One or more roles not found")

    user_internal_dict = user.model_dump()
    user_internal_dict["hashed_password"] = get_password_hash(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    try:
        user_internal = UserCreateInternal(**user_internal_dict)
        created_user: UserRead = await crud_users.create(db=db, commit=False, object=user_internal)
        await db.flush()
        print(created_user)

        # Add into user_role table (make relationship between user and role)
        for role in roles["data"]:
            user_role_internal_dict = {}
            user_role_internal_dict["user_id"] = created_user.id
            user_role_internal_dict["role_id"] = role["id"]
            user_role_internal_dict["created_by"] = current_user["id"]
            user_role_internal_dict["updated_by"] = current_user["id"]

            await crud_user_role.create(db=db, object=UserRoleCreateInternal(**user_role_internal_dict), commit=False)

        await db.commit()

        user_with_roles_internal_dict = UserRead(**(created_user.__dict__)).model_dump()
        user_with_roles_internal_dict["roles"] = roles["data"]

        print(user_with_roles_internal_dict)

        print(UserReadSub(**user_with_roles_internal_dict))
        return UserReadSub(**user_with_roles_internal_dict)
    except Exception as e:
        await db.rollback()
        return {"error": e.__repr__}


@router.get("/users")
async def read_users(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> PaginatedListResponse[UserReadSub]:
    users = await get_joined_users(db)
    response: dict[str, Any] = paginated_response(crud_data=users, page=page, items_per_page=items_per_page)
    return response


@router.get("/users/me")
async def read_users_me(request: Request, current_user: current_user_dependency, db: db_dependency) -> UserReadSub:
    user = await get_joined_users(db, get_one=True, id=current_user["id"])
    return user


@router.get("/users/{id}")
async def read_user(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int
):
    user = await get_joined_users(db=db, get_one=True, id=id)
    if not user:
        raise NotFoundException("User not found")
    return user


@router.patch("/users/{id}")
async def update_user(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int, values: UserUpdate
):
    user_exist = await crud_users.exists(db=db, id=id, is_deleted=False)
    if not user_exist:
        raise NotFoundException("User not found")
    
    user_internal_dict = values.model_dump(exclude_unset=True)
    user_internal_dict["updated_by"] = current_user["id"]

    await crud_users.update(db=db, object=UserUpdateInternal(**user_internal_dict), id=id)

    return {"status": "Update successfully"}


@router.delete("/users/{id}")
async def delete_user(
    request: Request, current_user: current_user_dependency, db: db_dependency,
    id: int
) -> dict[str, str]:
    user_exist = await crud_users.exists(db=db, id=id, is_deleted=False)
    if not user_exist:
        raise NotFoundException("User not found")

    await crud_users.delete(db=db, id=id, is_deleted=False)
    return {"message": "Delete Successfully"}


# ============= Local Helper =============
async def get_joined_users(db, get_one=False,**kwags):
    users = await crud_users.get_multi_joined(
        db=db,
        is_deleted=False,
        schema_to_select=UserReadSub,
        return_as_model=True,
        nest_joins=True,
        joins_config=[
            JoinConfig(
                model=UserRole,
                join_on=and_(User.id == UserRole.user_id, UserRole.is_deleted == False),
                join_prefix="user_role",
                schema_to_select=UserRoleRead,
                join_type="left",
                relationship_type="one-to-many",
            ),
            JoinConfig(
                model=Role,
                join_on=and_(UserRole.role_id == Role.id, Role.is_deleted == False),
                join_prefix="roles",
                schema_to_select=RoleRead,
                join_type="left",
                relationship_type="one-to-many",
            ),
        ],
        **kwags
    )

    for user in users["data"]:
        user.roles = remove_duplicates(user.roles)

    if (get_one):
        if not users["data"]:
            return None
        return users["data"][0]

    return users
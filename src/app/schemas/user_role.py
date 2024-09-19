from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import (
    CreatedTimestamp, 
    UpdatedTimestamp, 
    DeletedTimestamp, 
    UserCreateBy, 
    UserUpdatedBy
)


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleRead(CreatedTimestamp, UserRoleBase):
    id: int


class UserRoleCreate(UserRoleBase):
    model_config = ConfigDict(extra="forbid")


class UserRoleCreateInternal(UserCreateBy, UserRoleBase):
    ...


class UserRoleUpdate(UpdatedTimestamp):
    model_config = ConfigDict(extra="forbid")
    
    user_id: int
    role_id: int


class UserRoleUpdateInternal(UserUpdatedBy, UserRoleBase):
    ...


class UserRoleDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
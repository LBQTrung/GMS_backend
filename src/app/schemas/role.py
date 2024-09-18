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

class RoleBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["User Userson"])]


class RoleRead(RoleBase):
    id: int


class RoleCreate(CreatedTimestamp, RoleBase):
    model_config = ConfigDict(extra="forbid")


class RoleCreateInternal(UserCreateBy, RoleBase):
    ...


class RoleUpdate(UpdatedTimestamp):
    model_config = ConfigDict(extra="forbid")
    name: Annotated[ Optional[str]| None, Field(min_length=2, max_length=30, examples=["User Userson"])]


class RoleUpdateInternal(UserUpdatedBy, RoleBase):
    ...


class RoleDelete(DeletedTimestamp):
    model_config = ConfigDict(extra="forbid")
    ...
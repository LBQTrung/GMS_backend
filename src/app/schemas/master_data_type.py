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

class MasterDataTypeBase(BaseModel):
    code: Annotated[str, Field(min_length=2, max_length=30, examples=["master_data_type_code"])]
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["Master data type name"])]


class MasterDataTypeRead(MasterDataTypeBase):
    id: int


class MasterDataTypeCreate(CreatedTimestamp, MasterDataTypeBase):
    model_config = ConfigDict(extra="forbid")


class MasterDataTypeCreateInternal(UserCreateBy, MasterDataTypeBase):
    ...


class MasterDataTypeUpdate(UpdatedTimestamp):
    model_config = ConfigDict(extra="forbid")
    
    code: Annotated[ Optional[str]| None, Field(min_length=2, max_length=30, examples=["master_data_type_code"], default=None)] 
    name: Annotated[ Optional[str]| None, Field(min_length=2, max_length=30, examples=["Master data type name"], default=None)] 


class MasterDataTypeUpdateInternal(UserUpdatedBy, MasterDataTypeUpdate):
    ...


class MasterDataTypeDelete(DeletedTimestamp):
    model_config = ConfigDict(extra="forbid")
    
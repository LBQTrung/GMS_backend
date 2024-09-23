from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import (
    CreatedTimestamp, 
    UpdatedTimestamp, 
    DeletedTimestamp, 
    UserCreateBy, 
    UserUpdatedBy
)

class MasterDataBase(BaseModel):
    code: Annotated[str, Field(min_length=2, max_length=30, examples=["master_data_code"])]
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["Master data name"])]
    value: Annotated[str | None, Field(min_length=2, max_length=30, examples=["Value example"], default=None)]
    data: Annotated[dict | None, Field(default=None)]


class MasterDataRead(MasterDataBase):
    id: int


class MasterDataCreate(CreatedTimestamp, MasterDataBase):
    model_config = ConfigDict(extra="forbid")


class MasterDataCreateInternal(UserCreateBy, MasterDataBase):
    ...


class MasterDataUpdate(UpdatedTimestamp):
    model_config = ConfigDict(extra="forbid")
    
    code: Annotated[ Optional[str]| None, Field(min_length=2, max_length=30, examples=["master_data_type_code"], default=None)] 
    name: Annotated[ Optional[str]| None, Field(min_length=2, max_length=30, examples=["Master data type name"], default=None)] 
    value: Annotated[str | None, Field(min_length=2, max_length=30, examples=["Value example"], default=None)]
    data: Annotated[dict | None, Field(default=None)]

class MasterDataUpdateInternal(UserUpdatedBy, MasterDataUpdate):
    ...


class MasterDataDelete(DeletedTimestamp):
    model_config = ConfigDict(extra="forbid")
    
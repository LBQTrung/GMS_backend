import re
from datetime import datetime
from typing import Annotated, Union

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer, field_validator
from sqlalchemy import Date

from ..core.schemas import CreatedTimestamp, UpdatedTimestamp, DeletedTimestamp, UserCreateBy, UserUpdatedBy
from ..schemas.role import RoleRead


class UserBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["User Userson"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"])]
    date_of_birth: Annotated[Union[str, datetime, None], Field(examples=["yyyy-mm-dd"], default=None)]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    phone: Annotated[str | None, Field(min_length=10, max_length=10, examples=["0766635748"])]
    profile_image_url: Annotated[str, Field(default="https://www.profileimageurl.com")]

    @field_serializer("date_of_birth")
    def convert_dob(self, value):
        if isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d")
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d").date()
        return value
    
    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, value):
        if isinstance(value, str):
            if not re.match(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError('Date of birth must be in the format yyyy-mm-dd')
        return value


class UserRead(CreatedTimestamp, UserCreateBy, UserBase):
    id: int
    
    
class UserReadSub(UserRead):
    roles: list[RoleRead]


class UserCreate(CreatedTimestamp, UserBase):
    model_config = ConfigDict(extra="forbid")

    password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]
    roles: Annotated[list[int] | None, Field(examples=[1, 2, 3], default=[2])]


class UserCreateInternal(UserBase):
    hashed_password: str


class UserUpdate(UpdatedTimestamp, UserBase):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=2, max_length=30, examples=["User Userson"], default=None)]
    username: Annotated[str | None, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"], default=None)]
    date_of_birth: Annotated[Union[str, datetime, None], Field(examples=["yyyy-mm-dd"], default=None)]
    email: Annotated[EmailStr | None, Field(examples=["user.userson@example.com"], default=None)]
    phone: Annotated[str | None, Field(min_length=10, max_length=10, examples=["0766635748"], default=None)]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.profileimageurl.com"], default=None
        ),
    ]


class UserUpdateInternal(UserUpdatedBy, UserUpdate):
    ...


class UserDelete(DeletedTimestamp):
    model_config = ConfigDict(extra="forbid")

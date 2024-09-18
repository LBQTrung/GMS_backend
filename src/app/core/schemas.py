import uuid as uuid_pkg
from datetime import UTC, datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_serializer


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


# -------------- mixins --------------
class CreatedTimestamp(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_serializer("created_at")
    def serialize_dt(self, created_at: datetime | None, _info: Any) -> str | None:
        if created_at is not None:
            return created_at.isoformat()

        return None

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime | None, _info: Any) -> str | None:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class UpdatedTimestamp(BaseModel):
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime | None, _info: Any) -> str | None:
        if updated_at is not None:
            return updated_at.isoformat()

        return None


class DeletedTimestamp(BaseModel):
    deleted_at: datetime | None = Field(default=None)
    is_deleted: bool = False

    @field_serializer("deleted_at")
    def serialize_dates(self, deleted_at: datetime | None, _info: Any) -> str | None:
        if deleted_at is not None:
            return deleted_at.isoformat()

        return None

class UserCreateBy(BaseModel):
    created_by: int
    updated_by: int


class UserUpdatedBy(BaseModel):
    updated_by: int


class UserDeletedBy(BaseModel):
    deleted_by: int

    # Todo: Update delete by
    @field_serializer("deleted_by")
    def serialize_dates(self, deleted_at: datetime | None, _info: Any) -> str | None:
        ...


# -------------- token --------------
class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    username_or_email: str


class TokenBlacklistBase(BaseModel):
    token: str
    expires_at: datetime


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenBlacklistUpdate(TokenBlacklistBase):
    pass

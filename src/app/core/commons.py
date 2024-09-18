from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.dependencies import get_current_user
from ..core.db.database import async_get_db
from ..schemas.user import UserRead

#Todo: do later
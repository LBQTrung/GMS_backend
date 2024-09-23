from datetime import UTC, datetime

from sqlalchemy import DateTime, String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class MasterData(Base):
    __tablename__ = "master_data"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    code: Mapped[int] = mapped_column(String(30))
    name: Mapped[int] = mapped_column(String(30))
    value: Mapped[str] = mapped_column(String(20), nullable=True)
    data: Mapped[dict] = mapped_column(JSON, nullable=True)

    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

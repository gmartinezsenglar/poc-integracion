from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": "auth_users"}
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

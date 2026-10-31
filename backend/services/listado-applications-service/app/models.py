from datetime import datetime
from uuid import UUID
from sqlalchemy import String, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Base(DeclarativeBase):
    pass


class Listing(Base):
    __tablename__ = "publicaciones"
    __table_args__ = {"schema": "listado_applications"}
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    autor_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    titulo: Mapped[str] = mapped_column(String(140), nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)
    comuna: Mapped[str] = mapped_column(String(100), nullable=False)
    precio_clp: Mapped[int] = mapped_column(Integer, nullable=False)
    cupos_totales: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False, default="Compartida")
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="Disponible")
    fecha_publicacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

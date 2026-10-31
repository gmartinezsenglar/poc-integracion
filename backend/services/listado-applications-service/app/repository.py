from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Listing


class ListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, region: str | None, comuna: str | None, limit: int):
        statement = select(Listing).where(Listing.estado != "Cerrada")
        if region:
            statement = statement.where(Listing.region == region)
        if comuna:
            statement = statement.where(Listing.comuna == comuna)
        statement = statement.order_by(Listing.fecha_publicacion.desc(), Listing.id.desc()).limit(limit)
        return self.db.scalars(statement).all()

    def get(self, listing_id: UUID):
        return self.db.get(Listing, listing_id)

    def create(self, autor_id: UUID, **data):
        row = Listing(id=uuid4(), autor_id=autor_id, tipo="Compartida", estado="Disponible", **data)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

from datetime import datetime
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from .application import ListingService
from .config import Settings, get_settings
from .database import get_db
from .models import Listing
from .repository import ListingRepository
from .security import Identity, get_identity

app = FastAPI(title="Roomies PoC · Listado/Postulaciones", version="0.1.0")


class PublicationCreate(BaseModel):
    titulo: str = Field(min_length=5, max_length=140)
    region: str = Field(min_length=2, max_length=100)
    comuna: str = Field(min_length=2, max_length=100)
    precio_clp: int = Field(gt=0)
    cupos_totales: int = Field(ge=1, le=20)


class PublicationResponse(PublicationCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    autor_id: UUID
    tipo: str
    estado: str
    fecha_publicacion: datetime


def get_repo(db: Session = Depends(get_db)):
    return ListingRepository(db)


def get_service(repo: ListingRepository = Depends(get_repo), settings: Settings = Depends(get_settings)):
    return ListingService(repo, settings)


@app.get("/health", tags=["Infraestructura"])
def health():
    return {"status": "ok", "service": "listado-applications"}


@app.get("/publicaciones", response_model=list[PublicationResponse], tags=["Publicaciones"])
def list_publicaciones(
    region: str | None = None, comuna: str | None = None,
    limit: int = Query(default=40, ge=1, le=100),
    repo: ListingRepository = Depends(get_repo),
):
    return repo.list(region, comuna, limit)


@app.get("/publicaciones/{publicacion_id}", response_model=PublicationResponse, tags=["Publicaciones"])
def get_publicacion(publicacion_id: UUID, repo: ListingRepository = Depends(get_repo)):
    row = repo.get(publicacion_id)
    if not row:
        raise HTTPException(404, "Publicación no encontrada")
    return row


@app.post("/publicaciones/compartidas", response_model=PublicationResponse, status_code=201, tags=["Publicaciones"])
def create_publicacion(
    data: PublicationCreate, identity: Identity = Depends(get_identity),
    service: ListingService = Depends(get_service),
):
    return service.create(identity, data.model_dump())

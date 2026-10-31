from typing import Annotated
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from .application import ProfileService
from .config import Settings, get_settings
from .database import get_db
from .repository import ProfileRepository
from .security import Identity, get_identity

app = FastAPI(title="Roomies PoC · Auth/Users", version="0.1.0")


class ProfileUpdate(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)


class ProfileResponse(BaseModel):
    id: str
    nombre: str
    correo_verificado: bool


def get_service(db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> ProfileService:
    return ProfileService(ProfileRepository(db), settings)


@app.get("/health", tags=["Infraestructura"])
def health():
    return {"status": "ok", "service": "auth-users"}


@app.get("/usuarios/me", response_model=ProfileResponse, tags=["Usuarios"])
def get_me(identity: Identity = Depends(get_identity), service: ProfileService = Depends(get_service)):
    return service.get(identity)


@app.put("/usuarios/me", response_model=ProfileResponse, tags=["Usuarios"])
@app.patch("/usuarios/me", response_model=ProfileResponse, tags=["Usuarios"])
def save_me(data: ProfileUpdate, identity: Identity = Depends(get_identity), service: ProfileService = Depends(get_service)):
    return service.save(identity, data.nombre)

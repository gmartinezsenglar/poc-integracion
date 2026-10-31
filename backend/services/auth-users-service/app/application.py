import httpx
from fastapi import HTTPException
from .security import Identity
from .config import Settings
from .repository import ProfileRepository


def correo_confirmado(identity: Identity, settings: Settings) -> bool:
    if not settings.supabase_publishable_key:
        raise HTTPException(503, "Falta clave pública de Supabase para consultar usuario")
    try:
        response = httpx.get(
            f"{settings.supabase_url.rstrip('/')}/auth/v1/user",
            headers={"Authorization": f"Bearer {identity.bearer}", "apikey": settings.supabase_publishable_key},
            timeout=8,
        )
        if response.status_code == 401:
            raise HTTPException(401, "La sesión de Supabase no es válida")
        response.raise_for_status()
        user = response.json()
        if user.get("id") != str(identity.id):
            raise HTTPException(401, "El usuario del token no coincide con Supabase Auth")
        return bool(user.get("email_confirmed_at"))
    except HTTPException:
        raise
    except (httpx.HTTPError, ValueError):
        raise HTTPException(503, "No fue posible consultar Supabase Auth") from None


class ProfileService:
    def __init__(self, repository: ProfileRepository, settings: Settings):
        self.repository = repository
        self.settings = settings

    def get(self, identity: Identity):
        row = self.repository.get(identity.id)
        if row is None:
            raise HTTPException(404, "Completa primero tu perfil")
        return {"id": str(row.id), "nombre": row.nombre, "correo_verificado": correo_confirmado(identity, self.settings)}

    def save(self, identity: Identity, nombre: str):
        if not correo_confirmado(identity, self.settings):
            raise HTTPException(403, "Debes verificar tu correo antes de guardar el perfil")
        row = self.repository.upsert(identity.id, nombre)
        return {"id": str(row.id), "nombre": row.nombre, "correo_verificado": True}

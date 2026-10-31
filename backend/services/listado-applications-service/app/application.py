import httpx
from fastapi import HTTPException
from .config import Settings
from .repository import ListingRepository
from .security import Identity


class ListingService:
    def __init__(self, repository: ListingRepository, settings: Settings):
        self.repository = repository
        self.settings = settings

    def create(self, identity: Identity, data: dict):
        # Comunicación REAL entre microservicios. No hay acceso SQL a auth_users.
        try:
            response = httpx.get(
                f"{self.settings.auth_users_url.rstrip('/')}/usuarios/me",
                headers={"Authorization": f"Bearer {identity.bearer}"},
                timeout=12,
            )
        except httpx.TimeoutException:
            raise HTTPException(504, "Auth/Users tardó demasiado") from None
        except httpx.HTTPError:
            raise HTTPException(502, "No fue posible contactar Auth/Users") from None
        if response.status_code == 404:
            raise HTTPException(409, "Primero debes completar tu perfil")
        if response.status_code in (401, 403):
            raise HTTPException(response.status_code, "Autenticación rechazada por Auth/Users")
        if response.status_code != 200:
            raise HTTPException(502, "Auth/Users no está disponible para validar al autor")
        try:
            profile = response.json()
        except ValueError:
            raise HTTPException(502, "Respuesta inválida de Auth/Users") from None
        if profile.get("id") != str(identity.id) or profile.get("correo_verificado") is not True:
            raise HTTPException(403, "Perfil no válido o correo sin verificar")
        return self.repository.create(identity.id, **data)

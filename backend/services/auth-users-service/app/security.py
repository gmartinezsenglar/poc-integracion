from dataclasses import dataclass
from uuid import UUID

import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import Settings, get_settings

bearer = HTTPBearer(auto_error=False)
_jwks_clients: dict[str, PyJWKClient] = {}


@dataclass(frozen=True)
class Identity:
    id: UUID
    email: str
    bearer: str


def get_identity(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    settings: Settings = Depends(get_settings),
) -> Identity:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(401, "Falta token Bearer", headers={"WWW-Authenticate": "Bearer"})
    if not settings.supabase_url.startswith("https://"):
        raise HTTPException(503, "SUPABASE_URL no configurada")
    base = settings.supabase_url.rstrip("/")
    try:
        # PoC usa claves asimétricas Supabase (RS256 o ES256) y JWKS público.
        client = _jwks_clients.setdefault(
            base, PyJWKClient(f"{base}/auth/v1/.well-known/jwks.json", lifespan=300)
        )
        key = client.get_signing_key_from_jwt(creds.credentials).key
        claims = jwt.decode(
            creds.credentials,
            key=key,
            algorithms=["RS256", "ES256"],
            issuer=f"{base}/auth/v1",
            audience="authenticated",
            options={"require": ["sub", "exp", "iat", "iss", "aud"]},
            leeway=20,
        )
        if claims.get("role") != "authenticated":
            raise jwt.InvalidTokenError("No es token de usuario autenticado")
        return Identity(id=UUID(claims["sub"]), email=claims.get("email", ""), bearer=creds.credentials)
    except (jwt.PyJWTError, ValueError, KeyError):
        raise HTTPException(401, "Token inválido o expirado", headers={"WWW-Authenticate": "Bearer"}) from None
    except Exception:
        raise HTTPException(503, "No fue posible verificar la firma del token") from None

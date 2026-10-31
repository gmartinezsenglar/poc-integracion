import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_users_url: str = "http://localhost:8001"
    listado_url: str = "http://localhost:8002"
    cors_origins: str = "http://localhost:3000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
app = FastAPI(title="Roomies PoC · API Gateway", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_methods=["GET", "PUT", "PATCH", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/health", tags=["Infraestructura"])
def health():
    return {"status": "ok", "service": "gateway"}


@app.get("/ready", tags=["Infraestructura"])
async def ready():
    targets = {"auth-users": settings.auth_users_url, "listado": settings.listado_url}
    results = {}
    async with httpx.AsyncClient(timeout=5) as client:
        for name, url in targets.items():
            try:
                r = await client.get(f"{url.rstrip('/')}/health")
                results[name] = r.status_code == 200
            except httpx.HTTPError:
                results[name] = False
    ok = all(results.values())
    return JSONResponse({"status": "ok" if ok else "degraded", "services": results}, status_code=200 if ok else 503)


async def proxy(request: Request, upstream_base: str, path: str):
    # Solo se reenvían encabezados necesarios, nunca X-User-ID del cliente.
    headers = {}
    for key in ("authorization", "content-type"):
        if request.headers.get(key):
            headers[key] = request.headers[key]
    try:
        async with httpx.AsyncClient(timeout=25, follow_redirects=False) as client:
            response = await client.request(
                method=request.method,
                url=f"{upstream_base.rstrip('/')}{path}",
                params=request.query_params,
                content=await request.body(),
                headers=headers,
            )
        ctype = response.headers.get("content-type", "application/json").split(";")[0]
        return Response(content=response.content, media_type=ctype, status_code=response.status_code)
    except httpx.TimeoutException:
        return JSONResponse({"detail": "Tiempo de espera agotado en el servicio"}, status_code=504)
    except httpx.HTTPError:
        return JSONResponse({"detail": "Servicio aguas abajo no disponible"}, status_code=502)


@app.api_route("/usuarios/me", methods=["GET", "PUT", "PATCH"], tags=["Usuarios"])
async def usuarios_me(request: Request):
    return await proxy(request, settings.auth_users_url, "/usuarios/me")


@app.api_route("/publicaciones", methods=["GET"], tags=["Publicaciones"])
async def publicaciones(request: Request):
    return await proxy(request, settings.listado_url, "/publicaciones")


@app.api_route("/publicaciones/compartidas", methods=["POST"], tags=["Publicaciones"])
async def publicaciones_compartidas(request: Request):
    return await proxy(request, settings.listado_url, "/publicaciones/compartidas")


@app.api_route("/publicaciones/{publicacion_id}", methods=["GET"], tags=["Publicaciones"])
async def publicacion_detalle(publicacion_id: str, request: Request):
    return await proxy(request, settings.listado_url, f"/publicaciones/{publicacion_id}")

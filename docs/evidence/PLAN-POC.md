# Plan de PoC: Roomies Web → Gateway → Microservicios → Supabase

**Estado inicial:** No se ha revisado aún el código fuente actual de TI2. No hay despliegues verificados.

## Inventario necesario antes de programar

- Repositorio nuevo de la PoC: URL y árbol de archivos.
- Código TI2 Sprint 1: backend/main/main.py, auth_service/main.py, match_conexion_service/routes.py, rutas, schemas/models y archivos de dependencias. Ajustar según estructura real.
- Dockerfile y compose existentes, si los hay.
- Gateway/servicio de publicaciones existentes, si los hay.
- Variables de entorno actuales: **solo nombres, nunca valores secretos**.
- Contratos Swagger/OpenAPI actuales, si existen.
- Región objetivo de Render y Supabase; conexión IPv4/IPv6.

## Implementación mínima (Roomies reducido)

1. FastAPI `auth-users-service`: `GET /health`, `GET /usuarios/me`, `PATCH /usuarios/me`; persistencia del perfil en schema `auth_users` usando UUID `sub` de JWT verificado.
2. FastAPI `listado-applications-service`: `GET /health`, `GET /publicaciones`, `POST /publicaciones/arrendador`; persistencia en schema `listado_applications`.
3. Comunicación Listado→Auth/Users por HTTP al validar o consultar al autor, sin SELECT al schema ajeno.
4. Gateway FastAPI: proxy `/usuarios/*` y `/publicaciones/*`, headers Authorization, errores y timeout controlado.
5. Next.js: login Supabase Auth directo; consulta perfil, crea y lista publicaciones a través del Gateway.
6. Docker Compose en local y luego despliegues en Render + Vercel.
7. Opcional: Supabase Storage y Realtime como casos verticales adicionales.

## Matriz de evidencia

| ID | Prueba | Resultado esperado | Estado |
| --- | --- | --- | --- |
| P01 | Arrancar cada microservicio sin los demás | `/health` HTTP 200 | Pendiente |
| P02 | Abrir OpenAPI por servicio | `/docs` disponible | Pendiente |
| P03 | Probar Docker Compose | Arranque reproducible | Pendiente |
| P04 | JWT ausente / inválido | HTTP 401 | Pendiente |
| P05 | Crear perfil y recuperar tras reinicio | Persistencia real | Pendiente |
| P06 | Perfil y listado con roles distintos | Acceso autorizado solamente al schema propio | Pendiente |
| P07 | Intentar acceso a schema ajeno | Denegación comprobada | Pendiente |
| P08 | Gateway → ambos servicios | No importa módulos Python de otros servicios | Pendiente |
| P09 | Listado → Usuarios por HTTP | No accede a tablas ajenas | Pendiente |
| P10 | Error aguas abajo y timeout | No responde 200 engañoso | Pendiente |
| P11 | Auth Users en Render | URL funcional + logs + docs | Pendiente |
| P12 | Cold start | Medición de tiempo con método documentado | Pendiente |
| P13 | Next.js en Vercel → API Gateway Render | Flujo E2E persistido | Pendiente |
| P14 | Re-despliegue desde nuevo commit | Disponibilidad y persistencia verificadas | Pendiente |
| P15 | Variante privada o VPS | Probado o marcado explícitamente NO PROBADO | Pendiente |

## Recogida estándar de pruebas

Registrar `timestamp`, `git SHA`, servicio, endpoint, resultado esperado, HTTP observado, duración, errores/logs y captura. No guardar JWT, passwords ni connection strings en GitHub o capturas.

### Comandos de medición con PowerShell (Windows)

```powershell
curl.exe -sS -o NUL -w "HTTP %{http_code} | total %{time_total}s`n" https://TU-SERVICIO.onrender.com/health
```

Repetir tras un periodo de inactividad suficientemente largo para comprobar una posible suspensión. No deducir un cold start de una sola medición.

### Plantilla de prueba

```
ID:
Fecha/hora (zona horaria):
Commit SHA:
Servicio/versión:
Comando o pasos:
Esperado:
Observado (HTTP y segundos):
Evidencia/archivo de log:
Conclusión (acotada):
```

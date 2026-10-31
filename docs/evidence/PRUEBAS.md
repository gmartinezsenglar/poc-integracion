# Registro reproducible de evidencias · DEP-01 / DEP-02

No completar una casilla como «aprobada» si no se ejecutó la prueba en el entorno indicado.

| Prueba | Entorno | Resultado | Evidencia | Fecha |
|---|---|---|---|---|
| Auth/Users `/health` | Local TestClient | **OK**: 200 | `pytest tests/test_api.py` | 30-10-2026 |
| Listado `/health` | Local TestClient | **OK**: 200 | `pytest tests/test_api.py` | 30-10-2026 |
| Gateway `/health` | Local TestClient | **OK**: 200 | `pytest tests/test_gateway.py` | 30-10-2026 |
| Acceso sin Bearer a perfil | Local TestClient | **OK**: 401 | `test_requires_bearer` | 30-10-2026 |
| Acceso sin Bearer a crear publicación | Local TestClient | **OK**: 401 | `test_requires_bearer` | 30-10-2026 |
| Docker Compose completo | Windows del estudiante | PENDIENTE | — | — |
| JWT real desde Supabase Auth | Integración real | PENDIENTE | — | — |
| Perfil persistido en Supabase | Integración real | PENDIENTE | — | — |
| Publicación persistida en Supabase | Integración real | PENDIENTE | — | — |
| Aislamiento de schema/rol | Supabase | PENDIENTE | — | — |
| Gateway → Listado → Auth/Users | Render | PENDIENTE | — | — |
| `/docs` y `/health` remoto | Render | PENDIENTE | — | — |
| Cold start / latencia | Render | PENDIENTE | — | — |
| UI de Vercel usando API real | Vercel | PENDIENTE | — | — |
| Reimplementar/redesplegar y consultar datos previos | Render + Supabase | PENDIENTE | — | — |

## Tiempos medidos

Comando de PowerShell:

```powershell
curl.exe -sS -o NUL -w "HTTP %{http_code} | total %{time_total}s`n" https://TU-SERVICIO.onrender.com/health
```

Registrar ensayo, momento de inactividad, HTTP status, total en segundos, región, tipo de instancia. No tomar un solo resultado como tendencia.

## Registro de incidentes

| Fecha | Servicio | Problema observado | Causa probable | Cambio | Resultado verificado |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

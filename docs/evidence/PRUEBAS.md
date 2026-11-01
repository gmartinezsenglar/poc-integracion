# Registro reproducible de evidencias · DEP-01 / DEP-02

No completar una casilla como «aprobada» si no se ejecutó la prueba en el entorno indicado.

| Prueba | Entorno | Resultado | Evidencia | Fecha |
|---|---|---|---|---|
| Auth/Users `/health` | Local TestClient | **OK**: 200 | `pytest tests/test_api.py` | 30-10-2026 |
| Listado `/health` | Local TestClient | **OK**: 200 | `pytest tests/test_api.py` | 30-10-2026 |
| Gateway `/health` | Local TestClient | **OK**: 200 | `pytest tests/test_gateway.py` | 30-10-2026 |
| Acceso sin Bearer a perfil | Local TestClient | **OK**: 401 | `test_requires_bearer` | 30-10-2026 |
| Acceso sin Bearer a crear publicación | Local TestClient | **OK**: 401 | `test_requires_bearer` | 30-10-2026 |
| Docker `hello-world` | Windows del estudiante | **OK**: imagen descargada y contenedor ejecutado | Salida `Hello from Docker!` reportada por el estudiante | 31-10-2026 |
| Docker Compose completo | Windows del estudiante | PENDIENTE | — | — |
| JWT real desde Supabase Auth | Integración real | PENDIENTE | — | — |
| Perfil persistido en Supabase | Integración real | PENDIENTE | — | — |
| Publicación persistida en Supabase | Integración real | PENDIENTE | — | — |
| Creación de roles, schemas y tablas de PoC | Supabase SQL Editor | **OK**: script corregido ejecutado sin error | Captura `Success. No rows returned` | 31-10-2026 |
| Privilegios `SELECT` por schema/rol | Supabase SQL Editor | **OK**: `true, false, true, false` | Captura de consulta con `has_table_privilege` | 31-10-2026 |
| Acceso real como `poc_auth` | PostgreSQL de Supabase mediante Session Pooler | **OK**: `current_user = poc_auth`; lectura propia permitida; lectura del schema Listado denegada | Captura de `psql` interactivo por Docker con TLS 1.3 | 01-11-2026 |
| Acceso real como `poc_listado` | PostgreSQL de Supabase mediante Session Pooler | PENDIENTE (repetir prueba inversa con rol distinto) | — | — |
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
| 31-10-2026 | Supabase PostgreSQL | `ERROR 42501: must be able to SET ROLE "poc_auth"` | El SQL Editor no pudo asumir el rol creado | Script `002_supabase_setup.sql` adaptado: crear objetos sin `SET ROLE`, conceder privilegios explícitos | **OK**: creación y comprobación administrativa de permisos; conexión real comprobada después para `poc_auth`; `poc_listado` pendiente |

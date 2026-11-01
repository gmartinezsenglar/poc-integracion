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
| Inicio de sesión real de Supabase Auth desde Vercel | Web → Supabase Auth | **OK observado**: interfaz muestra sesión, UUID y correo confirmado tras corregir variables de entorno de Vercel; verificación del JWT en FastAPI pendiente | Captura del estudiante | 01-11-2026 |
| JWT verificado por FastAPI | Vercel → Gateway → Auth/Users | **OK en flujo autenticado observado**: GET y PUT de perfil de usuario con sesión de Supabase funcionaron, tras corregir DATABASE_URL | Captura de web con `Perfil encontrado en PostgreSQL` y confirmación en SQL | 01-11-2026 |
| Lectura de perfil `GET /usuarios/me` | Vercel → Gateway → Auth/Users → Supabase PostgreSQL | **OK observado**: inicialmente 404 por perfil inexistente; tras PUT la interfaz muestra `Perfil encontrado en PostgreSQL` | Capturas de Roomies PoC antes/después del guardado | 01-11-2026 |
| Perfil persistido en Supabase | Vercel → Gateway → Auth/Users → PostgreSQL | **OK comprobado**: se guardó perfil y el SQL Editor devolvió una fila en `auth_users.profiles` con UUID del usuario y nombre de prueba | Captura de interfaz `Perfil guardado` + consulta SQL con 1 fila | 01-11-2026 |
| Publicaciones consultadas mediante Gateway desde Vercel | Vercel → Gateway → Listado → PostgreSQL | **OK observado en UI**: dos publicaciones de prueba aparecen bajo `Publicaciones persistidas`; falta verificar filas mediante SQL directo y persistencia tras redespliegue | Capturas de la web con una y luego dos publicaciones | 01-11-2026 |
| Filas de publicaciones verificadas mediante SQL | Supabase SQL Editor | PENDIENTE de consulta directa sobre `listado_applications.publicaciones` | — | — |
| Creación de roles, schemas y tablas de PoC | Supabase SQL Editor | **OK**: script corregido ejecutado sin error | Captura `Success. No rows returned` | 31-10-2026 |
| Privilegios `SELECT` por schema/rol | Supabase SQL Editor | **OK**: `true, false, true, false` | Captura de consulta con `has_table_privilege` | 31-10-2026 |
| Acceso real como `poc_auth` | PostgreSQL de Supabase mediante Session Pooler | **OK**: `current_user = poc_auth`; lectura propia permitida; lectura del schema Listado denegada | Captura de `psql` interactivo por Docker con TLS 1.3 | 01-11-2026 |
| Acceso real como `poc_listado` | PostgreSQL de Supabase mediante Session Pooler | **OK**: `current_user = poc_listado`; lectura de Listado permitida; acceso a `auth_users` denegado | Captura `psql` por Docker postgres:17-alpine con TLS 1.3 | 01-11-2026 |
| Listado `/docs`, `/health`, `/publicaciones` | Render · listado-applications-service | **OK observado**: docs accesibles; health ok; listado devuelve `[]` (SELECT remoto sin publicaciones) | Capturas de URLs compartidas por el estudiante | 01-11-2026 |
| Gateway `/ready` | Render | **OK observado tras repetición**: `status=ok`, `auth-users=true`, `listado=true`; anteriormente `degraded` (posible suspensión por inactividad, no causa confirmada) | Capturas del estudiante de ambas respuestas | 01-11-2026 |
| Gateway → Listado → Auth/Users | Render | **Indicio funcional alto**: publicaciones nuevas visibles desde UI autenticada, pero no hay traza distribuida de la validación de autor; verificar en logs y SQL | Capturas de perfil y listado Vercel | 01-11-2026 |
| `/docs` y `/health` remoto | Render · auth-users-service | **OK observado por el usuario**: `/health` devolvió `status: ok` y `/docs` mostró Swagger/OpenAPI; no acredita acceso SQL | Captura y URLs compartidas en chat: `https://roomies-poc-auth-users.onrender.com/health`, `/docs` | 01-11-2026 |
| Cold start / latencia | Render | PENDIENTE | — | — |
| Next.js desplegado y accesible en Vercel | Vercel | **OK observado**: web pública activa con login Supabase, perfil almacenado y listado de publicaciones | Capturas del estudiante en `https://roomies-poc-web.vercel.app/` | 01-11-2026 |
| UI de Vercel usando Gateway y APIs reales | Vercel + Render | **OK observado**: perfil creado y recuperado; la web muestra dos publicaciones consultadas vía Gateway | Capturas de interfaz y de fila de perfil en SQL | 01-11-2026 |
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
| 01-11-2026 | Render Auth/Users | `GET /usuarios/me` devolvió HTTP 500 al intentar abrir conexión PostgreSQL | `DATABASE_URL` contenía el host literal `POOLER_HOST`, no el host de Session Pooler de Supabase | Estudiante corrigió `DATABASE_URL` en Render y volvió a consultar | **RESUELTO**: GET autenticado responde 404 esperado cuando aún no existe perfil |

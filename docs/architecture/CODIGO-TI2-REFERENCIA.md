# Estado del código oficial de TI2 vs. la PoC (30-10-2026)

Referencias revisadas: archivos ZIP de `dev-web` y `main` aportados por TI4, y repositorio público <https://github.com/Benjitapley/taller-de-integra->. Se trata de instantáneas; **no se ha modificado** el repositorio de TI2.

| Área | Observación en ZIP `dev-web` | PoC independiente |
|---|---|---|
| Autenticación | `backend/auth_service/main.py` implementa flujos propios, `security.py` firma/verifica JWT; importado desde `backend/main/main.py` | El cliente usa Supabase Auth directamente; FastAPI valida JWT asimétrico por JWKS |
| Backend principal | `backend/main/main.py` importa Auth y Match; mezcla funcionalidades en un FastAPI | Gateway y 2 FastAPI independientes, cada uno desplegable |
| Base de datos | Código actual menciona schema `haycupo` | Schemas `auth_users` y `listado_applications`, 1 rol/login por schema |
| Frontend | Existe `frontend-next/` Next.js con componentes y auth vía backend | Next.js básico directo a Supabase Auth y a Gateway |
| Despliegue | No se observaron Dockerfiles en el ZIP revisado | 3 Dockerfiles, compose y documentación Render |

La guía del Sprint 2 menciona `auth-users-service`, `listado-applications-service` y `api-gateway` como límites de responsabilidad. La PoC no es un migrador del código actual. Si se acuerda llevar estos cambios a TI2, debe hacerse mediante contrato OpenAPI, decisiones del equipo y Pull Requests independientes.

**Seguridad**: el ZIP de `main` contiene `.env`. No se reutilizó ni reprodujo su contenido. Evaluar rotación de credenciales si fueron publicadas o compartidas indebidamente.

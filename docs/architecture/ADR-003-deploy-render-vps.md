# ADR-003 — Despliegue de Roomies: Render versus VPS

- **Estado:** Propuesto / pendiente de evidencia
- **Fecha:** 2026-10-12
- **Responsables:** TI2-B (tarea oficial), TI4 (PoC complementaria y coordinación)
- **Tareas:** DEP-01, DEP-02, DB-01, DB-02, GATE-01, GATE-02
- **Versión / commit de la PoC:** PENDIENTE

## 1. Contexto

Roomies contempla aplicación web en Next.js/Vercel, API Gateway y microservicios FastAPI, además de Supabase Auth/PostgreSQL/Storage/Realtime. La PoC prueba el tramo web; la aplicación móvil queda fuera. La topología final y el modelo de base de datos **no** están decididos.

### Pregunta arquitectónica

¿Qué opción permite desplegar y operar los microservicios y el API Gateway de Roomies con disponibilidad, aislamiento, seguridad, costos y complejidad adecuados para el curso y sus próximos sprints?

## 2. Alternativas

- **A. Render, servicios web públicos (prueba gratuita):** Gateway + servicios accesibles mediante HTTPS y protegidos por autenticación/autorización. No se equipara a red privada.
- **B. Render, Gateway público y servicios internos (instancias que acepten conexiones privadas):** medir o dejar constancia de que la variante no se probó por costo.
- **C. VPS, Docker Compose + proxy HTTPS + servicios internos:** considerar tareas operativas (dominio, TLS, firewall, parches, observabilidad, copias de seguridad, recuperación).
- **D. Alternativa híbrida, si procede:** Vercel + Render/VPS + Supabase.

## 3. Criterios de evaluación

| Criterio | Render: evidencia/medida | VPS: evidencia/medida | Impacto / relevancia |
| --- | --- | --- | --- |
| Despliegue inicial | PENDIENTE | NO PROBADO / PENDIENTE | |
| Independencia de procesos | PENDIENTE | NO PROBADO / PENDIENTE | |
| Acceso por Gateway | PENDIENTE | NO PROBADO / PENDIENTE | |
| Comunicación entre servicios | PENDIENTE | NO PROBADO / PENDIENTE | |
| Networking público/privado | PENDIENTE | NO PROBADO / PENDIENTE | |
| Inicio en frío y latencia caliente | PENDIENTE | NO PROBADO / PENDIENTE | |
| Conexión Supabase Postgres y permisos | PENDIENTE | NO PROBADO / PENDIENTE | |
| Variables y secretos | PENDIENTE | NO PROBADO / PENDIENTE | |
| Logs y health checks | PENDIENTE | NO PROBADO / PENDIENTE | |
| Costo mensual total estimado | PENDIENTE | PENDIENTE | Declarar moneda y fecha |
| Mantenimiento y recuperación | PENDIENTE | PENDIENTE | |
| Requisitos del profesor: BD por servicio | PENDIENTE DE CONFIRMAR | PENDIENTE | Schema + rol ≠ BD independiente |

## 4. Pruebas ejecutadas

Por cada prueba guardar: **ID, fecha/hora y zona horaria, versión/commit, URL anonimizada si corresponde, pasos/comando, resultado esperado, resultado observado, tiempo en segundos, log/evidencia, responsable**.

| ID | Descripción | Esperado | Observado | Estado |
| --- | --- | --- | --- | --- |
| T01 | Auth Users remoto `/health` | HTTP 200 | PENDIENTE | Pendiente |
| T02 | Swagger remoto `/docs` | Disponible | PENDIENTE | Pendiente |
| T03 | JWT válido/incorrecto | 200/401 | PENDIENTE | Pendiente |
| T04 | Lectura/escritura de Postgres | Persiste tras redeploy | PENDIENTE | Pendiente |
| T05 | Acceso a schema ajeno | Denegado | PENDIENTE | Pendiente |
| T06 | Gateway → Auth Users | Respuesta correcta | PENDIENTE | Pendiente |
| T07 | Gateway → Listado | Respuesta correcta | PENDIENTE | Pendiente |
| T08 | Listado → Auth Users | HTTP entre microservicios | PENDIENTE | Pendiente |
| T09 | Gateway propaga fallo downstream | HTTP 502/503/504 apropiado | PENDIENTE | Pendiente |
| T10 | Render cold start tras inactividad | Latencia cuantificada | PENDIENTE | Pendiente |
| T11 | Next.js Vercel → Gateway → BD | Operación end-to-end | PENDIENTE | Pendiente |

## 5. Riesgos y restricciones

- Render Free entra en reposo por inactividad y no recibe tráfico por red privada (verificar documentación vigente al decidir).
- Los costos de varias instancias y el egreso de red pueden cambiar; registrar fuente y fecha.
- Supabase con schemas y roles separa lógicamente; no demuestra bases PostgreSQL independientes.
- La conexión Supabase puede requerir Session Pooler dependiendo de IPv4/IPv6.
- Exponer microservicios públicos obliga a no confiar ciegamente en el Gateway para la seguridad.
- Un VPS agrega operación: firewall, TLS, parcheo, monitoreo, backups y restauración.

## 6. Decisión

**PENDIENTE.** No elegir una plataforma antes de completar y analizar las pruebas relevantes. Indicar opción seleccionada, razones, supuestos y evidencia.

### Condiciones que cambiarían la decisión

- Exigencia docente de bases de datos físicas independientes.
- Necesidad de acceso privado entre servicios sin exponer endpoints.
- Restricciones de disponibilidad / latencia / costo que invalide la opción elegida.
- Número definitivo de microservicios en producción.

## 7. Consecuencias y próximos pasos

- Beneficios:
- Limitaciones:
- Cambios requeridos en CI/CD, Docker, DNS, seguridad y observabilidad:
- Responsable y fecha de revisión:

## 8. Fuentes

- Backlog TI2 Sprint 2, tareas DEP-01/02, DB-01/02, GATE-01/02.
- https://render.com/docs/free
- https://render.com/docs/private-network
- https://render.com/pricing
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://vercel.com/docs/monorepos

> Importante: resultados no probados se deben marcar «NO PROBADO», nunca «funciona» o «falla» por deducción.

# ADR-003 · Despliegue Roomies: Render versus VPS (PoC)

**Estado:** PENDIENTE DE DECISIÓN. **Fecha de borrador:** 30-10-2026.

## Contexto

TI2 requiere Dockerizar y desplegar un microservicio real (DEP-01), comprobar health, docs y cold start. DEP-02 requiere decidir topología final comparando Render/VPS con evidencia, una vez contrastada la estrategia de datos (DB-02). Una PoC de dos microservicios **no** representa por sí misma la operación de los cinco servicios definitivos.

## Opciones

1. **Render + Supabase + Vercel:** servicios desplegados separadamente y administrados; sencillo de operar, con restricciones del plan Free.
2. **VPS + Supabase + Vercel:** procesos/contenedores bajo responsabilidad del equipo; permite un reverse proxy y redes propias, requiere operación, TLS, seguridad, actualizaciones y monitoreo.
3. **Render híbrido:** Gateway público y servicios privados de pago (evaluar costo y regiones, sin asumir prueba realizada).

## Matriz a completar

| Factor | Render (evidencia) | VPS (evidencia o fuente) |
|---|---|---|
| Facilidad inicial | Pendiente | Pendiente |
| Número de contenedores para 5 servicios + Gateway | Pendiente | Pendiente |
| Comunicación HTTP interna | Free: no recibir privado; pendiente probar pública | Pendiente |
| Disponibilidad y cold start | Pendiente medir | Pendiente |
| Costos mensuales completos | Pendiente cotización real | Pendiente cotización real |
| Conexión y aislamiento en Supabase | Pendiente | Pendiente |
| Gestión de TLS, secretos, logs, backups | Pendiente | Pendiente |
| Carga operativa del equipo y seguridad | Pendiente | Pendiente |
| Cumplimiento de NFR-07 / NFR-16 / NFR-17 | Pendiente | Pendiente |

## Decisión provisional

**No decidida.** Una prueba exclusivamente en Render no demuestra automáticamente superioridad sobre VPS; si no se prueba VPS, señalar sus filas como «estimación documental». El profesor aceptó esquema + rol exclusivo dentro de una base Supabase; eso no obliga a usar una VPS para persistencia.

## Evidencias necesarias antes de cerrar

- URL remota, commits y logs de despliegue.
- `/health`, `/docs`, errores y timeout del Gateway.
- Medición cold/warm y comportamiento luego de 15 minutos sin solicitudes.
- Escritura/lectura persistida y prueba negativa de acceso a schema ajeno.
- Costos actuales para N servicios con estimación explícita.
- Evaluación del mantenimiento y cumplimiento para demo del curso.

## Consecuencias y riesgos

La infraestructura Free puede dormir durante la exposición, especialmente si varios servicios se reactivan en cascada. Los servicios internos de Render no están disponibles con las mismas características que los gratuitos. El costo de VPS puede parecer menor sin contabilizar tiempo de administración y seguridad.

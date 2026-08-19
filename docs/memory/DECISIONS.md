# Hato AI Architect — Decisiones

## D-001 — GitHub como memoria persistente
**Decisión:** usar el repositorio como almacenamiento persistente de código y memoria estructurada.

**Motivo:** preservar continuidad entre sesiones y mantener historial versionado.

## D-002 — No almacenar conversaciones completas
**Decisión:** la memoria debe contener conocimiento relevante extraído de los hilos, no copias indiscriminadas de conversaciones.

**Motivo:** los hilos pueden mezclar temas del proyecto con conversaciones ajenas.

## D-003 — Consolidación por clasificación
**Decisión:** clasificar la información en historia, arquitectura, decisiones, implementación, pruebas, problemas, soluciones, ideas, estado y próximos pasos.

**Motivo:** facilitar recuperación y evitar contaminación de la memoria.

## D-004 — MEMORY_CHECKPOINT
**Decisión:** introducir `MEMORY_CHECKPOINT` como punto de preservación del estado relevante de un hilo.

**Motivo:** evitar pérdida de conocimiento cuando el contexto crece o cuando se cambia de hilo.

## D-005 — Automatización posterior
**Decisión:** construir primero una memoria fundacional y un consolidador fiable; después automatizar el commit diario.

**Motivo:** la automatización debe preservar conocimiento correctamente antes de ejecutarse sin supervisión.

## D-006 — Finca como unidad productiva independiente
**Decisión:** en el vocabulario conceptual de Hato, `Finca` representa una unidad productiva ganadera independiente. No se adopta por defecto una jerarquía `Empresa → múltiples Fincas`.

**Motivo:** preservar el concepto original del sistema: una finca constituye por sí misma una explotación con sus animales, potreros, corrales, instalaciones, producción y operación. Cualquier modelo futuro de multiempresa deberá definirse explícitamente sin reinterpretar la finca como una simple sucursal.

**Referencia:** `docs/TERMINOLOGY.md`, versión 1.0.

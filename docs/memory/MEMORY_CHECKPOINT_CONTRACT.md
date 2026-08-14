# MEMORY_CHECKPOINT — Contrato

## Propósito
`MEMORY_CHECKPOINT` es un evento formal de preservación de memoria. Representa un punto verificable en el tiempo desde el cual Hato puede reconstruir el estado relevante del proyecto.

## Identidad
- `checkpoint_id`: identificador único. Formato recomendado: `MC-YYYY-MM-DD-NNN`.
- `timestamp`: fecha y hora exactas de creación del checkpoint en formato ISO-8601.
- `timezone`: zona horaria IANA usada para interpretar el timestamp.

## Trazabilidad
- `project`: proyecto al que pertenece.
- `source`: origen de la información (`conversation`, `manual`, `automatic`, etc.).
- `thread`: referencia al hilo o sesión cuando esté disponible.
- `parent_checkpoint`: checkpoint anterior relacionado, si existe.
- `commit_sha`: commit de GitHub asociado después de persistir el checkpoint.

## Estado
- `status`: estado del checkpoint, por ejemplo `draft`, `consolidated`, `persisted` o `superseded`.

## Contenido consolidado
El checkpoint puede contener solamente conocimiento relevante:
- contexto
- decisiones
- arquitectura
- implementación
- experimentos
- problemas
- soluciones
- ideas
- estado actual
- próximos pasos

## Reglas
1. Un hilo no equivale a memoria del proyecto.
2. No se almacenan conversaciones completas por defecto.
3. El contenido ajeno al proyecto se filtra.
4. La fecha y hora del checkpoint son metadatos generados al crear el evento, no inferidos de la conversación.
5. La fecha del evento y la fecha de consolidación pueden ser diferentes.
6. El checkpoint debe poder localizarse por `checkpoint_id`, fecha y commit.
7. La persistencia final debe quedar vinculada a un commit versionado.

## Relación con Git
El checkpoint es el evento lógico; el archivo Markdown es una representación legible; el commit de Git proporciona versionado y trazabilidad.

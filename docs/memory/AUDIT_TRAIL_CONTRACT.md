# Hato AI — Contrato de Audit Trail (2.10)

## Propósito

2.10 registra de forma trazable qué conocimiento entró al pipeline, qué clasificación recibió, qué comparación y resolución produjo, qué propuesta se generó y qué cambios fueron finalmente persistidos.

## Registro mínimo

```json
{
  "audit": {
    "id": "audit-...",
    "timestamp": "...",
    "pipeline_version": "...",
    "source_item_ids": [],
    "classification": {},
    "comparison": {},
    "conflict_resolution": {},
    "proposal_id": null,
    "approval": {},
    "persistence": {},
    "checkpoint_id": null,
    "result": "PERSISTED"
  }
}
```

## Eventos registrables

- `INGESTED`
- `STRUCTURED`
- `CLASSIFIED`
- `COMPARED`
- `CONFLICT_DETECTED`
- `CONFLICT_RESOLVED`
- `PROPOSAL_CREATED`
- `APPROVED`
- `REJECTED`
- `PERSISTED`
- `CHECKPOINT_CREATED`
- `FAILED`

## Reglas de integridad

1. Cada evento debe conservar timestamp, identidad del proceso y referencias de origen.
2. Los registros no deben ocultar decisiones ni errores.
3. Un evento de persistencia debe apuntar a la propuesta aprobada.
4. Un checkpoint posterior debe apuntar al registro de auditoría correspondiente.
5. El Audit Trail es histórico: no se reescribe para borrar decisiones anteriores.
6. Los fallos también se registran.
7. Los identificadores permiten reconstruir el recorrido de una unidad de conocimiento por el pipeline.
8. Información sensible no debe copiarse innecesariamente al registro; se guardan referencias cuando sea suficiente.

## Relación con 2.7–2.9

```text
2.7 PROPUESTA
      ↓
2.8 PERSISTENCIA
      ↓
2.10 AUDIT TRAIL
      ↓
2.9 CHECKPOINT POSTERIOR
```

El orden lógico de registro puede variar según la implementación, pero el resultado debe permitir reconstruir la cadena completa.

## Estado

**CERRADO — contrato de Audit Trail definido.**

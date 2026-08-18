# Hato AI — Contrato de Checkpoint Posterior (2.9)

## Propósito

2.9 crea un checkpoint después de una consolidación válida para garantizar un punto recuperable de continuidad.

## Precondiciones

Solo se genera cuando:

- la consolidación terminó correctamente;
- la persistencia autorizada terminó correctamente;
- no existe un fallo de integridad pendiente;
- el estado producido es coherente y trazable.

## Contenido mínimo

```json
{
  "checkpoint": {
    "id": "MC-YYYY-MM-DD-NNN",
    "created_at": "...",
    "trigger": "post_consolidation",
    "source_proposal_ids": [],
    "source_audit_ids": [],
    "memory_state": {
      "foundational": "...",
      "historical": "...",
      "checkpoints": "..."
    },
    "status": "VALID"
  }
}
```

## Reglas

1. Un checkpoint posterior no sustituye la memoria histórica.
2. Debe poder identificar la consolidación que lo produjo.
3. Debe ser inmutable una vez cerrado; una corrección genera un nuevo checkpoint.
4. Un checkpoint inválido nunca se presenta como punto de recuperación válido.
5. La numeración/identidad debe ser determinista y única.
6. Debe conservar referencias al Audit Trail.

## Destino

```text
docs/memory/checkpoints/
```

## Flujo

```text
2.8 PERSISTENCIA
      ↓
VALIDACIÓN
      ↓
2.9 CHECKPOINT POSTERIOR
      ↓
PUNTO DE RECUPERACIÓN
```

## Estado

**CERRADO — contrato de Checkpoint Posterior definido.**

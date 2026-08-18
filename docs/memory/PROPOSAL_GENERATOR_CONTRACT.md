# Hato AI — Contrato del Generador de Propuestas (2.7)

## 1. Propósito

El Generador de Propuestas recibe el resultado de 2.6 y construye una propuesta estructurada de actualización para que el siguiente componente pueda revisarla y, si corresponde, persistirla.

2.7 **no ejecuta cambios directamente**.

## 2. Entrada

Recibe:

- conocimiento nuevo estructurado;
- clasificación de 2.4;
- comparación de 2.5;
- resolución de conflictos de 2.6;
- referencias a memoria afectada;
- procedencia y confianza.

## 3. Salida contractual

```json
{
  "proposal": {
    "id": "proposal-...",
    "action": "CREATE",
    "target": "docs/memory/PROJECT_HISTORY.md",
    "reason": "Nueva decisión validada que debe incorporarse al historial.",
    "changes": [
      {
        "operation": "ADD",
        "content": "..."
      }
    ],
    "source_item_ids": ["item-001"],
    "affected_memory_ids": [],
    "review_required": false,
    "confidence": 0.95,
    "status": "PROPOSED"
  }
}
```

## 4. Acciones permitidas

- `CREATE` — proponer nueva entrada.
- `UPDATE` — proponer actualización de entrada existente.
- `OBSOLETE` — proponer marcar una entrada como obsoleta.
- `APPEND_HISTORY` — agregar información al historial sin borrar lo anterior.
- `NO_CHANGE` — no proponer modificación cuando sea duplicado o irrelevante.
- `REVIEW` — generar propuesta pendiente de revisión.

## 5. Reglas de seguridad

1. Una propuesta nunca equivale a aprobación.
2. No modifica `memory/` ni `docs/memory/` directamente.
3. No elimina información histórica.
4. Toda modificación debe indicar su destino y operaciones concretas.
5. Debe conservar las referencias al conocimiento de origen.
6. Una propuesta de Memoria Fundacional requiere revisión explícita.
7. Una contradicción no resuelta debe generar `REVIEW`.
8. Una propuesta debe ser reproducible a partir de la entrada recibida.

## 6. Flujo

```text
2.6 RESOLUCIÓN
      ↓
2.7 GENERADOR DE PROPUESTA
      ↓
PROPUESTA ESTRUCTURADA
      ↓
APROBACIÓN / REVISIÓN
      ↓
2.8 PERSISTENCIA CONTROLADA
```

## 7. Estado

**CERRADO — contrato del Generador de Propuestas definido.**

El cierre formaliza la salida que 2.8 puede aceptar sin permitir que 2.7 escriba directamente en memoria.

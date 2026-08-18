# Hato AI — Contrato de Resolución de Conflictos (2.6)

## 1. Propósito

2.6 recibe las comparaciones de 2.5 que indiquen conflicto y determina cómo debe tratarse la discrepancia sin destruir la memoria histórica ni sobrescribir silenciosamente decisiones.

El contrato del Consolidador establece que las contradicciones requieren revisión y que los cambios no deben sobrescribirse silenciosamente. fileciteturn6file0

## 2. Tipos de conflicto

- `DIRECT_CONTRADICTION` — dos afirmaciones incompatibles sobre el mismo conocimiento.
- `VERSION_CHANGE` — el conocimiento nuevo reemplaza legítimamente una versión anterior.
- `SCOPE_CONFLICT` — ambas afirmaciones son válidas pero aplican a contextos diferentes.
- `TEMPORAL_CONFLICT` — la diferencia depende del momento o vigencia.
- `UNCERTAIN_CONFLICT` — evidencia insuficiente para resolver.

## 3. Resultado

La resolución puede producir:

- `KEEP_EXISTING` — conservar conocimiento vigente.
- `ACCEPT_NEW` — aceptar conocimiento nuevo como vigente.
- `KEEP_BOTH_VERSIONED` — conservar ambos con contexto, alcance o temporalidad explícitos.
- `MARK_OBSOLETE` — marcar el conocimiento anterior como obsoleto sin eliminarlo.
- `REQUIRE_REVIEW` — detener la resolución automática y solicitar validación.
- `PROPOSE_FOUNDATIONAL_UPDATE` — proponer actualización de Memoria Fundacional, nunca ejecutarla automáticamente.

## 4. Reglas de decisión

1. Una contradicción no se resuelve mediante borrado.
2. Una decisión explícita y validada tiene mayor autoridad que una propuesta.
3. Una fuente posterior no gana automáticamente si su confianza es menor o su procedencia es insuficiente.
4. Cuando el contexto explica la aparente contradicción, se conserva la información con alcance diferenciado.
5. Cuando existe una evolución real del conocimiento, el elemento anterior pasa a histórico/obsoleto y el nuevo puede quedar vigente.
6. Cuando no existe evidencia suficiente, el resultado obligatorio es `REQUIRE_REVIEW`.
7. La Memoria Fundacional requiere validación explícita para cualquier promoción o modificación.
8. Todo resultado debe conservar las referencias de origen y de los elementos en conflicto.

## 5. Salida contractual

```json
{
  "conflict_resolution": {
    "conflict_type": "VERSION_CHANGE",
    "resolution": "MARK_OBSOLETE",
    "existing_memory_ids": ["memory-001"],
    "new_item_id": "item-042",
    "review_required": false,
    "confidence": 0.91,
    "reason": "La evidencia nueva establece una versión posterior del mismo conocimiento."
  }
}
```

## 6. Flujo

```text
2.5 COMPARADOR
      ↓
CONTRADICTION / UPDATE / OBSOLETE
      ↓
2.6 RESOLUCIÓN
      ↓
DECISIÓN DE TRATAMIENTO
      ↓
CONSOLIDADOR
      ↓
PERSISTENCIA + HISTORIAL + COMMIT
```

## 7. Límites

2.6 no debe:

- borrar memoria histórica;
- modificar directamente Memoria Fundacional sin validación;
- ocultar contradicciones;
- inventar evidencia;
- convertir automáticamente una propuesta en decisión.

## 8. Estado

**CERRADO — contrato de Resolución de Conflictos definido.**

El cierre formaliza la política de resolución y deja preparada la implementación posterior de reglas deterministas, heurísticas o IA bajo los mismos límites.

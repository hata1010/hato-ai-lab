# Hato AI — Contrato de Persistencia Controlada (2.8)

## 1. Propósito

2.8 recibe únicamente propuestas aprobadas y escribe de forma controlada la información autorizada en `memory/` y/o `docs/memory/`.

## 2. Entrada

Una propuesta válida de 2.7 debe contener como mínimo:

- identificador de propuesta;
- acción;
- destino;
- operaciones de cambio;
- conocimiento de origen;
- referencias a memoria afectada;
- estado de aprobación;
- confianza.

## 3. Estados de autorización

Solo una propuesta en estado `APPROVED` puede entrar al proceso de escritura.

Estados no persistibles:

- `PROPOSED`
- `REVIEW`
- `REJECTED`
- `INVALID`

## 4. Reglas de persistencia

1. Nunca escribir directamente una propuesta no aprobada.
2. Validar destino antes de escribir.
3. Impedir rutas fuera de `memory/` y `docs/memory/` para operaciones de memoria.
4. No borrar historia como efecto secundario de una actualización.
5. Las actualizaciones deben conservar trazabilidad hacia la versión anterior.
6. Los conflictos no resueltos no pueden persistirse como verdad consolidada.
7. La Memoria Fundacional requiere autorización explícita adicional.
8. Cada persistencia debe generar registro de auditoría.
9. Cada escritura debe poder asociarse a una propuesta y a sus fuentes.
10. Una operación inválida debe fallar de forma segura sin aplicar cambios parciales.

## 5. Destinos

### Memoria fundacional

```text
memory/
```

Para conocimiento estable y aprobado.

### Memoria evolutiva / histórica

```text
docs/memory/
```

Para decisiones, cambios, descubrimientos, estado, aprendizajes, experimentos e historia del proyecto.

### Checkpoints

```text
docs/memory/checkpoints/
```

Para puntos de continuidad previamente autorizados.

## 6. Flujo transaccional

```text
PROPUESTA 2.7
      ↓
VALIDAR APROBACIÓN
      ↓
VALIDAR DESTINO
      ↓
VALIDAR OPERACIONES
      ↓
PREPARAR CAMBIO
      ↓
APLICAR ATÓMICAMENTE
      ↓
AUDITAR
      ↓
COMMIT / RESULTADO
```

Ante un fallo de validación, no se debe dejar una actualización parcial.

## 7. Resultado

```json
{
  "persistence": {
    "proposal_id": "proposal-001",
    "status": "PERSISTED",
    "targets": ["docs/memory/PROJECT_HISTORY.md"],
    "operations_applied": 1,
    "audit_id": "audit-...",
    "commit": null
  }
}
```

El campo `commit` puede quedar pendiente cuando la persistencia y el commit Git sean responsabilidades separadas.

## 8. Límites

2.8 no clasifica conocimiento, no resuelve contradicciones y no inventa propuestas. Solo ejecuta propuestas aprobadas que cumplan el contrato.

## 9. Estado

**CERRADO — contrato de Persistencia Controlada definido.**

El cierre establece una frontera segura entre propuesta y escritura real en memoria.

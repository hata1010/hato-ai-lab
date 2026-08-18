# Hato AI — Contrato del Estructurador (2.3)

## 1. Propósito

El Estructurador convierte la salida normalizada del Extractor Semántico (2.2) en un contrato JSON determinista que pueda consumir el Consolidador.

No interpreta nuevamente la conversación ni decide la persistencia. Su responsabilidad es **dar forma, validar y hacer trazable** la información extraída.

## 2. Entrada

Recibe una colección de unidades extraídas por 2.2. Cada unidad puede representar, como mínimo:

- decisión;
- hecho/descubrimiento;
- cambio;
- objetivo;
- restricción;
- arquitectura;
- implementación;
- problema;
- solución;
- experimento;
- aprendizaje;
- estado;
- próximo paso;
- propuesta.

## 3. Salida contractual

La salida es un objeto JSON con esta forma lógica:

```json
{
  "schema_version": "1.0",
  "source": {
    "type": "conversation",
    "session": null,
    "timestamp": null
  },
  "project": "hato-ai-lab",
  "items": [
    {
      "id": "stable-item-id",
      "type": "decision",
      "content": "...",
      "status": "active",
      "confidence": 1.0,
      "provenance": {
        "source": "conversation",
        "session": null,
        "timestamp": null
      }
    }
  ]
}
```

## 4. Campos obligatorios

### Documento

- `schema_version`
- `source`
- `project`
- `items`

### Unidad de conocimiento

- `id`
- `type`
- `content`
- `status`
- `confidence`
- `provenance`

## 5. Tipos permitidos

El campo `type` debe pertenecer al vocabulario controlado del Consolidador. Como conjunto inicial:

`decision`, `fact`, `discovery`, `change`, `objective`, `constraint`, `architecture`, `implementation`, `problem`, `solution`, `experiment`, `learning`, `state`, `next_step`, `proposal`.

## 6. Reglas deterministas

1. No se inventa conocimiento que no exista en la extracción.
2. No se mezclan unidades independientes en una sola unidad salvo que la extracción las haya relacionado explícitamente.
3. Cada unidad conserva procedencia.
4. `confidence` debe ser numérico entre `0.0` y `1.0`.
5. `status` representa el estado de la unidad, no el resultado de comparación con memoria existente.
6. El Estructurador no determina `NUEVO`, `ACTUALIZACIÓN`, `DUPLICADO`, `CONTRADICCIÓN` u `OBSOLETO`; esa responsabilidad pertenece al Consolidador.
7. Una entrada inválida no se transforma silenciosamente: debe producir error de validación o quedar marcada como inválida.
8. La estructura debe ser serializable como JSON válido y estable entre ejecuciones equivalentes.

## 7. Identidad

`id` debe ser estable para permitir que el Consolidador compare una unidad con memoria existente. La implementación puede utilizar un identificador determinista derivado de tipo, contenido normalizado y procedencia.

## 8. Contrato con el Consolidador

El flujo queda definido así:

```text
2.1 Entrada de conocimiento
        ↓
2.2 Extractor semántico
        ↓
2.3 Estructurador
        ↓
JSON CONTRACT
        ↓
Consolidador
        ↓
Comparación / clasificación / destino
        ↓
Persistencia + Git
```

El Consolidador recibe exclusivamente unidades estructuradas conforme a este contrato cuando la ruta 2.3 esté activa.

## 9. Validación mínima

Antes de entregar la salida al Consolidador se comprueba:

- existencia de los campos obligatorios;
- tipos de datos válidos;
- vocabulario `type` permitido;
- `confidence` dentro de rango;
- procedencia presente;
- JSON serializable.

## 10. Estado de cierre de 2.3

**Estado: CERRADO — contrato estructural definido.**

Este cierre significa que la interfaz entre Extracción Semántica y Consolidador queda formalizada. No implica que la extracción semántica automática 2.2 esté implementada de forma autónoma.

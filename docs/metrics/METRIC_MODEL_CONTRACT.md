# Hato AI — Modelo de Métrica (3.1)

## Propósito

3.1 define qué es una métrica dentro de Hato AI y establece el contrato base que utilizarán el DSL, parser, validador, motor de cálculo, catálogo y trazabilidad.

## Definición

Una métrica es una **definición reproducible de una magnitud calculable**, aplicada sobre un contexto y un período determinados, cuyo resultado tiene una unidad y cuya obtención puede ser explicada y trazada.

Una métrica no es solamente un número: es la definición que permite producir ese número.

## Componentes obligatorios

```json
{
  "id": "metric-id",
  "name": "nombre_estable",
  "version": "1.0",
  "description": "Qué representa la métrica.",
  "entity": "finca",
  "formula": "total_leche / numero_vacas",
  "unit": "litros/vaca",
  "periodicity": "month",
  "context": {},
  "inputs": [],
  "status": "active"
}
```

### `id`
Identificador estable de la métrica.

### `name`
Nombre legible y estable dentro del catálogo.

### `version`
Versión de la definición. Un cambio semántico debe generar una nueva versión.

### `description`
Explicación humana del significado de la métrica.

### `entity`
Entidad principal sobre la que se calcula: por ejemplo `finca`, `potrero`, `animal`, `raza` o `especie`.

### `formula`
Expresión declarativa que define el cálculo. Su sintaxis será formalizada posteriormente por el DSL 3.2.

### `unit`
Unidad del resultado. Debe poder validarse semánticamente cuando el DSL y el motor lo permitan.

### `periodicity`
Frecuencia o granularidad temporal de cálculo.

### `context`
Filtros, dimensiones y condiciones que delimitan el cálculo.

### `inputs`
Datos o métricas de las que depende la fórmula.

### `status`
Estado de la definición: `draft`, `active`, `deprecated` o `disabled`.

## Periodicidad inicial

El vocabulario inicial contempla:

- `instant`
- `day`
- `week`
- `month`
- `quarter`
- `year`
- `custom`

El significado exacto de cada período será definido por el motor temporal 3.7.

## Contexto

El contexto permite expresar sobre qué subconjunto se calcula una métrica. Ejemplo conceptual:

```json
{
  "finca_id": "F001",
  "especie": "bovino",
  "sexo": "H",
  "period": "2026-08"
}
```

El contexto forma parte de la trazabilidad del resultado y no debe confundirse con la definición de la métrica.

## Tipos de métricas

El modelo inicial permite:

- `aggregate` — suma, promedio, mínimo, máximo, conteo, etc.;
- `ratio` — relación entre magnitudes;
- `rate` — magnitud por unidad de tiempo o entidad;
- `derived` — depende de otras métricas;
- `indicator` — métrica utilizada como indicador de gestión.

El tipo puede ampliarse sin romper el contrato base.

## Invariantes

1. Una métrica debe tener una definición estable y versionada.
2. El resultado siempre debe conservar unidad, contexto y período.
3. Una fórmula no debe depender de código arbitrario en la definición declarativa.
4. Los cambios semánticos requieren nueva versión.
5. Una métrica activa debe ser validable antes de ejecutarse.
6. Toda ejecución futura deberá poder señalar qué versión de la métrica produjo el resultado.
7. Una métrica puede depender de otras métricas, pero el ciclo de dependencias debe ser rechazado por el motor.

## Relación con la Fase 3

```text
3.1 MODELO DE MÉTRICA
        ↓
3.2 DSL
        ↓
3.3 PARSER
        ↓
3.4 VALIDACIÓN
        ↓
3.5 CÁLCULO
        ↓
3.6 DEPENDENCIAS
        ↓
3.7 TIEMPO + 3.8 CONTEXTO
        ↓
3.9 CATÁLOGO
        ↓
3.10 TRAZABILIDAD
```

## Estado

**CERRADO — Modelo de Métrica 3.1 definido y formalizado.**

El cierre establece el contrato conceptual y estructural; no implica todavía la implementación del DSL ni del motor de cálculo.

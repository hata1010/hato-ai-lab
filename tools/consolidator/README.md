# Hato AI — Consolidador Determinista

Fase 1 del Consolidador de memoria de Hato AI.

## Propósito

Esta primera implementación no intenta interpretar lenguaje natural ni tomar decisiones arquitectónicas. Proporciona un núcleo determinista para estructurar conocimiento previamente identificado y clasificar su destino.

## Flujo

```text
ENTRADA
  ↓
RELEVANCIA
  ↓
CLASIFICACIÓN
  ↓
COMPARACIÓN
  ↓
DESTINO
  ↓
RESULTADO TRAZABLE
```

## Entradas

El módulo recibe un documento JSON con:

- `source`: procedencia de la información;
- `timestamp`: momento de captura;
- `session`: identificador opcional de sesión;
- `items`: unidades de conocimiento ya extraídas.

Cada elemento puede contener:

```json
{
  "id": "obs-001",
  "text": "Falta un archivo de contexto rápido",
  "classification": "observation",
  "relevant": true,
  "existing_matches": [],
  "confidence": 0.9
}
```

## Clasificaciones iniciales

- `fact`
- `observation`
- `proposal`
- `decision`
- `discovery`
- `architecture`
- `implementation`
- `problem`
- `solution`
- `experiment`
- `learning`
- `state`
- `next_step`
- `open_question`

## Estados de comparación

- `new`
- `update`
- `duplicate`
- `contradiction`
- `obsolete`
- `unverified`

## Principio de esta fase

El Consolidador determinista **no crea archivos de memoria ni modifica Memoria Fundacional automáticamente**. Produce un resultado estructurado para revisión y para las siguientes capas del sistema.

La interpretación semántica y la extracción desde conversación pertenecen a fases posteriores.

## Ejecución

Desde la raíz del repositorio:

```bash
python tools/consolidator/consolidator.py entrada.json
```

También puede utilizarse `-` para recibir JSON desde stdin.

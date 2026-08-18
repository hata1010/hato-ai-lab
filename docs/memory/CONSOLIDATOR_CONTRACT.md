# Hato AI — Contrato del Consolidador

## 1. Propósito

El Consolidador transforma conocimiento producido durante la colaboración humano–IA en memoria estructurada, trazable y persistente.

Su misión es **capturar lo importante sin convertir toda conversación en memoria**.

## 2. Entrada

El Consolidador recibe, cuando estén disponibles:

- conversación o sesión de trabajo;
- contexto del proyecto;
- memoria existente;
- estado actual del repositorio.

El estado del repositorio debe considerarse una fuente de verdad técnica cuando exista riesgo de desfase entre la conversación y el proyecto real.

## 3. Relevancia

Primero determina si el contenido pertenece realmente a Hato AI.

- **Relevante:** continúa el proceso.
- **No relevante:** se descarta y no se incorpora a la memoria del proyecto.

## 4. Extracción

El Consolidador no copia conversaciones completas. Extrae unidades de conocimiento, entre ellas:

- decisión;
- descubrimiento;
- arquitectura;
- implementación;
- problema;
- solución;
- experimento;
- aprendizaje;
- estado;
- próximo paso.

## 5. Comparación con memoria existente

Cada elemento nuevo debe compararse con el conocimiento ya persistido.

Resultados posibles:

- **NUEVO** — conocimiento no registrado.
- **ACTUALIZACIÓN** — amplía o modifica conocimiento existente.
- **DUPLICADO** — ya está representado.
- **CONTRADICCIÓN** — entra en conflicto con conocimiento existente y requiere revisión.
- **OBSOLETO** — conocimiento anterior que debe conservarse como historia, pero cuya vigencia ha cambiado.

Los cambios y contradicciones no deben sobrescribirse silenciosamente.

## 6. Clasificación y destino

### Memoria Evolutiva

Ubicación principal:

```text
docs/memory/
```

Registra historia, descubrimientos, experimentos, aprendizajes, evolución, estado, problemas y soluciones.

### MEMORY_CHECKPOINT

Ubicación:

```text
docs/memory/checkpoints/
```

Se utiliza para preservar puntos significativos de continuidad y recuperación.

### Memoria Fundacional

Ubicación:

```text
memory/
```

Contiene conocimiento consolidado, estable y de mayor autoridad.

El conocimiento evolutivo **no se convierte automáticamente** en conocimiento fundacional.

## 7. Validación

El nivel de validación depende del destino:

- **Memoria Evolutiva:** puede registrarse automáticamente cuando cumple las reglas de relevancia y trazabilidad.
- **MEMORY_CHECKPOINT:** puede generarse automáticamente cuando se cumplen las condiciones definidas para un punto de continuidad.
- **Memoria Fundacional:** requiere validación explícita antes de incorporarse.

El Consolidador puede formular una propuesta de promoción a Memoria Fundacional, pero no debe ejecutarla por sí mismo.

## 8. Persistencia

Una incorporación validada debe quedar persistida y trazable:

```text
CONOCIMIENTO
      ↓
DOCUMENTO
      ↓
GIT
      ↓
COMMIT
```

Los cambios relevantes deben poder identificarse posteriormente mediante el historial del repositorio.

## 9. Reglas de integridad

El Consolidador no debe:

- borrar memoria histórica;
- sobrescribir silenciosamente decisiones;
- convertir cualquier conversación en conocimiento permanente;
- promover automáticamente conocimiento a Memoria Fundacional;
- modificar arquitectura fundamental sin validación;
- perder la procedencia del conocimiento.

El Consolidador sí debe:

- preservar historia;
- detectar cambios;
- identificar contradicciones;
- evitar duplicados;
- mantener procedencia;
- distinguir evolución de conocimiento consolidado.

## 10. Procedencia

Siempre que sea posible, cada unidad consolidada debe conservar información que permita responder:

> **¿De dónde salió este conocimiento?**

La estructura futura deberá contemplar, según corresponda:

```text
source
timestamp
session
classification
status
confidence
validated_by
```

La procedencia permite reconstruir el camino:

```text
CONVERSACIÓN
     ↓
DESCUBRIMIENTO
     ↓
MEMORIA EVOLUTIVA
     ↓
VALIDACIÓN
     ↓
MEMORIA FUNDACIONAL
```

## 11. Arquitectura conceptual

```text
                    CONVERSACIÓN
                         │
                         ▼
                   CONSOLIDADOR
                         │
                         ▼
                    RELEVANCIA
                         │
                  ┌──────┴──────┐
                  │             │
                NO             SÍ
                  │             │
               DESCARTAR        ▼
                           EXTRACCIÓN
                                │
                                ▼
                           CLASIFICACIÓN
                                │
                                ▼
                           COMPARACIÓN
                                │
                     ┌──────────┼──────────┐
                     │          │          │
                     ▼          ▼          ▼
                 EVOLUTIVA  CHECKPOINT  PROPUESTA
                                            │
                                            ▼
                                      VALIDACIÓN
                                            │
                                            ▼
                                    FUNDACIONAL
                                            │
                                            ▼
                                       PERSISTIR
                                            │
                                            ▼
                                         COMMIT
```

## 12. Evolución de implementación

El Consolidador se implementará por etapas:

### Fase 1 — Consolidador determinista

Clasificación básica, reglas de destino y persistencia controlada.

### Fase 2 — Consolidador asistido por IA

Análisis semántico de sesiones y extracción de conocimiento.

### Fase 3 — Consolidador inteligente

Detección de contradicciones, duplicados, cambios y propuestas de promoción.

### Fase 4 — Consolidador autónomo controlado

Automatización de tareas permitidas manteniendo límites, trazabilidad y validación para la Memoria Fundacional.

## 13. Principio rector

> **La memoria evolutiva registra cómo Hato aprende; la memoria fundacional conserva aquello que Hato ha consolidado como conocimiento.**

La transición entre ambas requiere filtrado, clasificación y validación.

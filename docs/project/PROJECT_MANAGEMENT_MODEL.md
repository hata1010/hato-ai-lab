# Modelo de Gestión del Proyecto — Hato AI Lab

**Estado:** Aprobado para uso operativo
**Fecha:** 2026-08-20
**Versión:** 1.0

## 1. Propósito

Este documento establece el modelo de gestión utilizado para planificar, ejecutar, medir y dar seguimiento al desarrollo de Hato AI Lab.

El modelo es **Agile híbrido adaptado a Hato AI Lab**, utilizando principios ágiles, elementos de Scrum para la ejecución iterativa y una estructura de fases/macrofases propia del producto.

No se pretende aplicar Scrum de forma dogmática. Scrum es un marco de trabajo y permite que el equipo defina prácticas y herramientas dentro de ese marco. La adaptación se realiza para conservar trazabilidad, cuantificación y control del alcance del proyecto.

## 2. Referencias metodológicas

- Agile Practice Guide — Project Management Institute (PMI): referencia para selección y adaptación de ciclos de vida ágiles, predictivos e híbridos, entrega de valor y medición.
- Scrum Guide 2020 — Ken Schwaber y Jeff Sutherland: referencia para Product Goal, Product Backlog, Sprint Goal, Increment, inspección y adaptación.
- Principios del Manifiesto Ágil: referencia para entrega incremental, colaboración, software funcional y respuesta al cambio.

## 3. Estructura de control

El proyecto se controla en cinco niveles:

1. **Product Goal:** estado futuro que Hato pretende alcanzar.
2. **Alcance Maestro:** límites funcionales y tecnológicos del producto.
3. **Fases:** grandes agrupaciones de entregables relacionados.
4. **Backlog / tareas:** trabajo concreto necesario para completar las fases.
5. **Iteraciones / Sprints:** ciclos cortos de ejecución, prueba, revisión y adaptación.

### Regla fundamental

**Una fase no es un Sprint.** Una fase puede contener varios Sprints y una tarea pertenece a una fase concreta.

## 4. Product Goal de Hato AI Lab

Construir un sistema integral de gestión ganadera que permita administrar de forma segura una o múltiples fincas, gestionar ganado, territorio, salud, recursos y producción, calcular indicadores mediante un motor de métricas trazable y generar información útil para la toma de decisiones, manteniendo documentación, auditoría y continuidad humano–IA.

El Product Goal define el horizonte del producto. El detalle del backlog puede evolucionar conforme se aprende durante la implementación.

## 5. Principio de alcance por etapas

Hato se desarrollará incrementalmente. El hecho de que una capacidad pertenezca a la visión futura **no significa que deba estar incluida en la primera etapa**.

El alcance se divide en etapas para evitar introducir complejidad tecnológica antes de que el núcleo operativo esté estabilizado.

## 6. Límite explícito de la Primera Etapa

La **Primera Etapa de Hato AI Lab** se concentra en construir y estabilizar el sistema digital base y la gestión ganadera/territorial mediante datos introducidos y administrados por el usuario o por procesos manuales controlados.

### Fuera del alcance de la Primera Etapa

No se implementará como requisito de esta etapa:

- sensores físicos de campo;
- RFID operativo automatizado;
- ESP32 u otros nodos de captura automática;
- LoRa u otra red de sensores;
- geolocalización automática de animales;
- seguimiento GPS automático en tiempo real;
- captura automática de posiciones de animales o maquinaria;
- automatización de movimientos basada directamente en sensores.

Estas capacidades quedan **reservadas para una Segunda o Tercera Etapa**, según la evolución del producto y la decisión de alcance correspondiente.

Esto no impide que la arquitectura actual conserve puntos de integración preparados para futuras fuentes automáticas de datos cuando exista una necesidad real.

## 7. Dominios funcionales previstos

El producto completo contempla, como mínimo, los siguientes dominios:

- Núcleo y seguridad multi-finca.
- Gestión ganadera.
- Territorio y potreros.
- Salud animal.
- Producción y métricas.
- Recursos e inventario.
- Gestión económica.
- Documentación y reportes.
- Analítica avanzada.
- Inteligencia y automatización.
- Continuidad, auditoría y memoria humano–IA.

Los dominios son componentes del producto. **No todos constituyen por sí mismos una fase.** Las fases se definirán según entregables, dependencias y objetivos de producto.

## 8. Fases

Las fases se establecen desde el alcance maestro y no se crean simplemente porque aparezca una nueva funcionalidad.

Una fase debe tener:

- objetivo;
- alcance;
- entregables;
- tareas;
- dependencias;
- criterios de terminado;
- pruebas/evidencia;
- estado;
- porcentaje de avance.

### Regla de creación de fases

Una nueva necesidad se incorpora primero al backlog y se evalúa contra las fases existentes. Solo se crea una nueva fase cuando la necesidad representa un bloque de producto suficientemente independiente, con objetivo y entregables propios.

## 9. Estados de tareas

| Estado | Significado |
|---|---|
| BACKLOG | Identificada, todavía no preparada para ejecución |
| READY | Lista para ejecutarse |
| IN_PROGRESS | En ejecución |
| REVIEW | Implementada, pendiente de revisión/prueba |
| DONE | Terminada y validada con evidencia |
| BLOCKED | No puede continuar por una dependencia o impedimento |
| CANCELLED | Retirada del alcance |

## 10. Identificación de tareas

Cada tarea debe tener un identificador único:

`HATO-Fxx-Tyyy`

Ejemplo:

`HATO-F06-T003`

- `HATO`: proyecto.
- `F06`: fase 6.
- `T003`: tarea 3 dentro de la fase.

## 11. Cuantificación

El seguimiento debe distinguir entre **avance de implementación** y **avance validado**.

Una tarea no se considera 100% terminada únicamente porque exista código. Para alcanzar `DONE` debe existir evidencia apropiada, como pruebas, validación funcional, documentación o commit verificable según el tipo de tarea.

### Avance de una fase

El porcentaje de una fase se calculará a partir de sus tareas ponderadas. Cuando no exista una ponderación especial, se utilizará el peso uniforme de las tareas.

### Avance global

El porcentaje global se calculará a partir del peso de las fases, no de una impresión subjetiva.

**No se permitirá declarar 100% del proyecto solamente porque las fases actualmente trabajadas estén completas.**

## 12. Evidencia

Cada tarea completada debe poder relacionarse con una evidencia verificable cuando corresponda:

- commit;
- prueba automatizada;
- prueba funcional;
- documento;
- captura o demostración;
- decisión registrada;
- revisión técnica.

La evidencia permite reconstruir por qué una tarea fue marcada como terminada.

## 13. Sprints / iteraciones

Los Sprints serán ciclos de trabajo para ejecutar un subconjunto del backlog y producir un incremento usable.

Cada Sprint debe tener un objetivo concreto. El contenido exacto puede ajustarse durante la ejecución sin perder el objetivo del Sprint.

Al finalizar cada iteración se realizará:

1. revisión del resultado;
2. pruebas;
3. actualización del estado de tareas;
4. registro de decisiones/cambios relevantes;
5. adaptación del siguiente trabajo.

## 14. Seguimiento del proyecto

La estructura de seguimiento prevista en el repositorio es:

```text
docs/project/
├── PROJECT_MANAGEMENT_MODEL.md
├── PROJECT_SCOPE.md
├── ROADMAP.md
├── PHASES.md
├── TASK_REGISTER.md
└── STATUS.md
```

Estos archivos serán la base documental para saber qué se pretende construir, cómo se divide, qué tareas existen y cuál es el avance real.

## 15. Regla de arranque de cada jornada

Al iniciar una jornada de trabajo:

1. recuperar la memoria canónica del repositorio;
2. consultar el estado de fases y tareas;
3. identificar pendientes reales;
4. revisar únicamente errores o bloqueos actuales;
5. seleccionar el trabajo del día;
6. ejecutar;
7. probar;
8. actualizar estado y evidencia;
9. cerrar la jornada con memoria y trazabilidad.

No se repetirán verificaciones de infraestructura o capacidades ya declaradas operativas salvo que exista evidencia de cambio o fallo.

## 16. Principio de no expansión accidental

Una funcionalidad nueva no amplía automáticamente el alcance de la etapa actual.

Antes de incorporarla se determina:

- si pertenece a una fase existente;
- si debe entrar al backlog futuro;
- si requiere una nueva fase;
- si pertenece a una etapa posterior.

En particular, la automatización mediante sensores y geolocalización automática queda explícitamente fuera de la Primera Etapa y deberá evaluarse como parte de la Segunda o Tercera Etapa.

## 17. Criterio de éxito del modelo

El modelo se considera funcional si permite responder en cualquier momento, usando únicamente la documentación y evidencia del repositorio:

- ¿Cuál es el objetivo del producto?
- ¿Cuál es el alcance actual?
- ¿Qué fases existen?
- ¿Qué fases están completas?
- ¿Qué porcentaje real lleva cada fase?
- ¿Qué tareas están pendientes?
- ¿Qué está bloqueado?
- ¿Qué se hizo durante la última jornada?
- ¿Qué evidencia demuestra que algo está terminado?
- ¿Qué queda fuera de la etapa actual?

## 18. Regla de adaptación

Este modelo puede evolucionar si la experiencia demuestra que una práctica no funciona. Los cambios deben registrarse como decisión de proyecto y no realizarse de forma silenciosa.

La prioridad es mantener **seguimiento simple, cuantificable, verificable y útil para tomar decisiones**.

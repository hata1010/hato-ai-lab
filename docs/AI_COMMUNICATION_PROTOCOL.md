# Protocolo de Comunicación y Diccionario de Conceptos — Hato AI Lab

**Versión:** 1.0  
**Estado:** Vigente  
**Propósito:** establecer un lenguaje común y reglas de trabajo para cualquier IA que participe en Hato AI Lab.

## 1. Propósito

Este documento evita ambigüedades entre personas e IAs. Define conceptos, responsabilidades, estados, entregables y reglas mínimas de comunicación.

El repositorio **Hato AI Lab** es la fuente de verdad técnica y documental del proyecto. La conversación sirve para coordinar el trabajo, pero una decisión o conocimiento que deba conservarse debe quedar registrado en el repositorio.

## 2. Principios de trabajo

1. **Planificación primero:** se ejecuta la subtarea prevista antes de avanzar a la siguiente.
2. **No reabrir trabajo cerrado:** una subtarea marcada como completada no se modifica salvo que aparezca una evidencia concreta de error o una nueva decisión formal.
3. **Evidencia sobre suposición:** las afirmaciones sobre código, modelos, archivos o funcionamiento deben basarse en inspección real del repositorio o pruebas.
4. **Cambio mínimo:** modificar solamente lo necesario para cumplir la subtarea actual.
5. **Cierre verificable:** toda subtarea debe terminar con resultado, evidencia, estado y pendientes.
6. **Replanificación ante errores:** si aparece un problema que invalida un nodo posterior, se vuelve al punto donde apareció el problema, se corrige y se replanifica desde allí.
7. **Separación de roles:** los nombres internos usados por el equipo humano para coordinar agentes no forman parte de la arquitectura ni de la documentación pública del proyecto.

## 3. Diccionario de conceptos

### Proyecto
**Hato AI Lab:** laboratorio y repositorio de memoria, arquitectura, decisiones, contratos, documentación y artefactos técnicos del sistema Hato.

### Repositorio / fuente de verdad
El estado registrado en GitHub es la referencia oficial para conocer qué existe, qué fue decidido y qué está vigente.

### Fase
Bloque mayor de trabajo dentro de la planificación. Ejemplo: **Fase 3 — Catálogo y Primera Familia de Métricas**.

### Subtarea
Unidad concreta de trabajo dentro de una fase. Tiene objetivo, alcance, entregable y condición de cierre.

### Nodo
Punto de la planificación que debe completarse antes de continuar. Si un nodo posterior revela un error originado en uno anterior, se regresa al nodo responsable del error.

### IA participante
Cualquier sistema de IA que intervenga en análisis, diseño, implementación, revisión, pruebas o documentación. El término es deliberadamente genérico.

### Dirección / arquitectura
Responsabilidad de mantener coherencia global del proyecto, controlar el alcance, interpretar resultados y decidir si se continúa, se corrige o se replanifica.

### Trabajo cerrado
Subtarea cuyo entregable fue revisado y aceptado. No debe ser alterada por iniciativa propia.

### Evidencia
Resultado verificable: archivo inspeccionado, código existente, prueba ejecutada, salida observada, commit, error reproducible o referencia documental.

### Entregable
Resultado concreto que produce una subtarea. Puede ser código, documentación, pruebas, inventario, contrato, configuración o evidencia.

### Estado
Clasificación del trabajo. Valores recomendados:
- `PENDIENTE`
- `EN_PROGRESO`
- `COMPLETADO`
- `BLOQUEADO`
- `REQUIERE_CORRECCION`
- `DESCARTADO`

### Decisión
Elección técnica o de alcance que afecta el proyecto y que debe conservarse cuando tenga valor futuro.

### Contrato
Definición formal de reglas que una implementación debe respetar. Un contrato no es una sugerencia.

### Modelo de datos
Estructura persistente que representa entidades y relaciones del dominio, incluyendo modelos Django y sus campos.

### Métrica
Resultado cuantificable definido por una fuente de datos, operaciones, filtros, agrupaciones, parámetros y reglas de cálculo.

### Función de métrica
Componente reutilizable que realiza una operación elemental o especializada dentro del cálculo de una métrica.

### DSL de métricas
Lenguaje o estructura declarativa utilizada para expresar cómo se compone y evalúa una métrica sin acoplarla innecesariamente a una vista concreta.

### Catálogo de métricas
Listado oficial de métricas conocidas, con código, nombre, familia, fuente, operación, parámetros, estado y prioridad.

### Métrica V1
Métrica seleccionada para formar parte de la primera familia oficial implementable y verificable con los datos y capacidades definidos para V1.

### Prototipo
Implementación experimental utilizada para validar una idea. No se considera automáticamente parte del producto ni del motor oficial.

### Mockup / prueba visual
Artefacto utilizado para validar interfaz, flujo o concepto visual. No debe confundirse con lógica funcional de producción.

### Motor de métricas
Conjunto de componentes responsables de interpretar, componer y ejecutar métricas.

### Memoria del proyecto
Conjunto de documentos del repositorio que conservan contexto, decisiones, arquitectura, estado e historia necesarios para la continuidad del trabajo.

## 4. Protocolo de comunicación

Cuando una IA recibe una subtarea debe:

1. **Identificar la fase y subtarea exactas.**
2. **Leer el contexto relevante del repositorio antes de modificar nada.**
3. **Determinar el alcance y no extenderlo sin justificación.**
4. **Inspeccionar el código/documentación necesarios para producir evidencia.**
5. **Ejecutar el trabajo solicitado.**
6. **Verificar el resultado mediante pruebas o inspección.**
7. **Informar claramente:**
   - qué se encontró;
   - qué se hizo;
   - qué archivos fueron afectados;
   - qué pruebas/evidencias existen;
   - qué quedó pendiente;
   - estado final de la subtarea.

No debe responder únicamente con teoría cuando la subtarea exige implementación o generación de código.

## 5. Regla de continuidad

Una IA no debe asumir que el chat contiene todo el conocimiento del proyecto. Antes de tomar decisiones técnicas debe consultar la memoria y los contratos relevantes del repositorio.

Si existe contradicción entre una suposición de la IA y evidencia actual del repositorio, prevalece la evidencia y debe reportarse la contradicción.

## 6. Regla de control de alcance

Si la planificación indica:

`3.1 → 3.2 → 3.3 → 3.4`

y 3.1, 3.2 y 3.3 están cerradas, no se deben reabrir para continuar con 3.4.

Solo se reabre una subtarea anterior cuando una evidencia posterior demuestra que existe un error real que afecta su validez. En ese caso se documenta:

- origen del problema;
- nodo afectado;
- impacto;
- corrección necesaria;
- nueva ruta de trabajo.

## 7. Regla para código

Cuando la tarea solicite código:

- entregar código ejecutable o archivos completos cuando corresponda;
- indicar exactamente dónde debe integrarse;
- no sustituir implementación por pseudocódigo si no fue solicitado;
- no modificar componentes fuera del alcance;
- conservar compatibilidad con contratos y modelos vigentes;
- realizar pruebas mínimas antes del cierre.

## 8. Regla para métricas

Toda métrica candidata debe poder describirse mediante, como mínimo:

- `codigo`
- `nombre`
- `familia`
- `fuente`
- `campo(s)`
- `operacion`
- `filtros`
- `agrupacion`, si aplica
- `parametros`, si aplica
- `unidad`
- `estado`
- `prioridad`
- `dependencias`
- `evidencia`

Una métrica no se considera implementada únicamente porque exista en un documento, mockup o ejemplo HTML.

## 9. Protocolo de cierre

El cierre de una subtarea debe utilizar esta estructura:

```text
SUBTAREA: <identificador>
ESTADO: <estado>

OBJETIVO:
<qué debía conseguirse>

RESULTADO:
<qué se consiguió>

CAMBIOS:
<archivos y componentes modificados>

EVIDENCIA:
<pruebas, inspecciones o resultados>

PENDIENTES:
<solo lo que realmente queda pendiente>

SIGUIENTE NODO:
<subtarea siguiente según planificación>
```

## 10. Regla de lenguaje

La documentación del proyecto debe utilizar términos genéricos y funcionales. No deben registrarse nombres internos utilizados por el equipo humano para identificar agentes concretos, salvo que exista una razón arquitectónica explícita.

El objetivo es que cualquier IA futura pueda incorporarse al proyecto leyendo este protocolo y la memoria, sin depender de conocer conversaciones privadas anteriores.

## 11. Regla final

**Primero se entiende el estado real. Luego se ejecuta la tarea. Después se verifica. Finalmente se registra el conocimiento que deba sobrevivir.**

No se agregan pasos, requisitos o trabajo fuera de la planificación sin una razón técnica verificable.

# Protocolo de Comunicación y Diccionario Común — IA 1 / Hato AI Lab

**Estado:** Vigente  
**Propósito:** establecer un lenguaje técnico común y un protocolo operativo para la comunicación entre el Humano, IA 1 y las demás IAs que participen en Hato AI Lab.

---

## 1. Principio fundamental

El repositorio **Hato AI Lab** es la fuente de verdad técnica, histórica y conceptual del proyecto.

La conversación sirve para coordinar el trabajo, pero las decisiones, contratos, definiciones y entregables que deban sobrevivir a una sesión deben quedar registrados en el repositorio.

IA 1 **no debe asumir que una palabra, modelo, métrica o estado significa algo distinto de lo definido aquí**. Si encuentra una contradicción real, debe señalarla antes de reinterpretarla.

---

## 2. Roles de comunicación

### Humano

- Define objetivos y prioridades.
- Decide cambios de alcance.
- Aprueba o rechaza decisiones relevantes.
- No está obligado a revisar todo el código fuente producido por las IAs.

### IA 1 — Implementación / análisis del repositorio

- Inspecciona directamente el repositorio cuando se le solicite.
- Produce análisis técnicos y, cuando el nodo lo indique, código real.
- Debe distinguir siempre entre **existente**, **prototipo**, **propuesto**, **pendiente** y **descartado**.
- No debe declarar implementado algo que solamente haya descrito conceptualmente.
- Debe informar archivos concretos afectados cuando produzca cambios.

### IA de control / cierre

- Verifica que el entregable corresponda al nodo de trabajo solicitado.
- Lee entre líneas inconsistencias, dependencias o estados incorrectamente clasificados.
- Decide si el nodo puede cerrarse o si existe una incidencia que obliga a corregirlo.
- No debe reabrir nodos anteriores sin una causa técnica explícita.

---

## 3. Regla de flujo de trabajo

El proyecto se ejecuta por nodos numerados de una planificación.

**Regla:** si un nodo está correctamente cerrado, no se vuelve a trabajar sobre él por iniciativa propia.

Si aparece un error en un nodo posterior:

1. se registra el error;
2. se identifica el nodo donde apareció;
3. se corrige desde ese punto;
4. solamente se reabre un nodo anterior si la evidencia demuestra que su resultado era incorrecto o incompatible.

Esto evita ciclos innecesarios y mantiene la trazabilidad del proyecto.

---

## 4. Contrato de comunicación con IA 1

Cada solicitud de trabajo a IA 1 debe contener, cuando corresponda:

```text
NODO: <identificador>
OBJETIVO: <qué debe producir>
ENTRADAS AUTORIZADAS: <documentos, código o resultados previos>
ALCANCE: <qué sí debe hacer>
NO HACER: <qué queda fuera del nodo>
ENTREGABLE: <resultado esperado>
CRITERIO DE CIERRE: <cómo saber que terminó>
```

### Reglas obligatorias

1. **No expandir el alcance.** IA 1 no debe convertir una subtarea en una investigación general.
2. **No rehacer nodos cerrados.** Solo hacerlo si existe una contradicción técnica demostrable.
3. **Separar análisis de implementación.** Si el nodo pide análisis, no presentar literatura como si fuera código.
4. **Si se pide código, entregar código.** Deben indicarse archivos, funciones/clases y pruebas realizadas.
5. **No inventar componentes.** Un modelo, campo, función o archivo solo puede declararse existente después de inspeccionarlo.
6. **No confundir factibilidad con implementación.** “Se puede construir” no significa “está construido”.
7. **No ocultar incertidumbre.** Si no puede verificar algo, debe marcarlo como no verificado.
8. **Respetar el diccionario de datos de este documento.**

---

# 5. Diccionario de conceptos del proyecto

## 5.1 Proyecto

| Término | Definición oficial |
|---|---|
| **Hato AI Lab** | Repositorio y espacio de memoria técnica, conceptual e histórica del proyecto Hato. |
| **Hato** | Sistema de gestión ganadera desarrollado con Django y sus componentes asociados. |
| **Fuente de verdad** | Estado registrado en el repositorio, priorizado sobre recuerdos de conversación o suposiciones. |
| **Nodo** | Unidad concreta de trabajo dentro de la planificación. |
| **Fase** | Conjunto ordenado de nodos relacionados con un objetivo mayor. |
| **Entregable** | Resultado verificable que permite cerrar un nodo. |
| **Cierre** | Confirmación de que el entregable satisface el criterio definido para el nodo. |
| **Incidencia** | Problema técnico o inconsistencia que impide continuar correctamente. |
| **Replanificación** | Modificación controlada del flujo debido a una incidencia real. |

---

## 5.2 Estados técnicos

| Estado | Significado |
|---|---|
| **EXISTENTE** | El componente está presente en el repositorio y fue verificado. |
| **FUNCIONAL** | Está implementado y existe evidencia de ejecución correcta. |
| **PARCIAL** | Existe implementación, pero no cubre todo el contrato requerido. |
| **PROTOTIPO** | Fue construido para experimentar o validar una idea, pero no es necesariamente parte del producto final. |
| **MOCKUP** | Representación visual o estática sin lógica productiva equivalente. |
| **PROPUESTO** | Diseño o especificación todavía no implementado. |
| **PENDIENTE** | Trabajo identificado que aún debe realizarse. |
| **EN TRANSICIÓN** | Existe una implementación anterior que debe converger hacia un contrato nuevo. |
| **DESCARTADO** | Se decidió que no forma parte de la solución vigente. |
| **NO VERIFICADO** | Se menciona o supone, pero no se inspeccionó evidencia suficiente. |

**Regla:** nunca utilizar “funcional”, “implementado” o “existente” como sinónimos de “propuesto”.

---

# 6. Diccionario de datos de Hato

## 6.1 Entidades principales

| Entidad | Significado |
|---|---|
| **Finca** | Unidad territorial/productiva principal a la que pertenecen los datos ganaderos. |
| **Potrero** | Unidad territorial interna de una finca destinada al manejo/pastoreo. |
| **Animal** | Individuo ganadero registrado en Hato. |
| **PesajeAnimal** | Registro histórico de peso de un animal asociado a una fecha. |
| **MovimientoAnimal** | Registro del movimiento de un animal hacia/desde un potrero u otra ubicación operacional. |
| **EventoSalud** | Registro de un evento sanitario asociado a un animal. |
| **Adquisicion** | Registro de adquisición/compra de ganado u otros elementos según el modelo vigente. |
| **Raza** | Catálogo de razas utilizado por los animales. |
| **TipoPasto** | Catálogo del tipo de pasto asociado a potreros. |

### Regla de identificación

Los nombres anteriores son nombres de dominio. No deben sustituirse por nombres inventados o equivalentes ambiguos en especificaciones o código.

---

## 6.2 Conceptos del motor de métricas

| Término | Definición |
|---|---|
| **Métrica** | Cálculo de dominio que transforma datos de Hato en un resultado interpretable. |
| **Código de métrica** | Identificador único y estable de una métrica, por ejemplo `PESO_ACTUAL`. |
| **Fuente** | Entidad/modelo desde donde se obtienen los datos de una métrica. |
| **Campo** | Atributo concreto utilizado como entrada. |
| **Filtro** | Condición aplicada al conjunto de datos antes de calcular. |
| **Agrupación** | División del conjunto por una dimensión, por ejemplo sexo o raza. |
| **Operación** | Transformación matemática o agregación aplicada a los datos. |
| **Composición** | Encadenamiento de funciones o métricas para producir otra métrica. |
| **Métrica atómica** | Métrica que obtiene su resultado mediante una operación directa sobre una fuente. |
| **Métrica derivada** | Métrica cuyo resultado depende de otras métricas, variables o cálculos. |
| **Serie temporal** | Conjunto ordenado de valores asociados a instantes/fechas, no un único escalar. |
| **Unidad** | Unidad física, temporal, monetaria o porcentual del resultado. |
| **Resultado escalar** | Un único valor como número, porcentaje, fecha o texto estructurado. |
| **Dato faltante** | Entrada necesaria que no existe para efectuar el cálculo. |
| **Regla de validación** | Condición que determina si una entrada o resultado es aceptable. |

---

# 7. Vocabulario oficial de operaciones del motor

| Operación | Significado |
|---|---|
| **CONTEO / COUNT** | Número de elementos/registros que cumplen las condiciones. |
| **SUMA / SUM** | Suma de valores numéricos. |
| **PROMEDIO / AVG** | Media aritmética de valores numéricos válidos. |
| **MIN** | Valor mínimo. |
| **MAX** | Valor máximo. |
| **FILTRO / FILTER** | Selección de elementos que cumplen condiciones. |
| **MAPEAR / MAP** | Aplicación de una función a cada elemento de una colección. |
| **LAST / ÚLTIMO** | Obtención del registro más reciente según la dimensión temporal definida. |
| **FIRST / PRIMERO** | Obtención del registro más antiguo según la dimensión temporal definida. |
| **DIRECTO** | Obtención directa de un valor sin agregación adicional. |
| **DIFERENCIA** | Resta entre dos valores compatibles. |
| **DIFERENCIA_FECHAS** | Diferencia temporal entre dos fechas/instantes. |

Cuando una implementación use nombres Python diferentes, la documentación debe indicar claramente su correspondencia con este vocabulario.

---

# 8. Diccionario de métricas V1 actualmente acordadas

Estas son las métricas seleccionadas en la Fase 3.3 como conjunto inicial V1. Su presencia en este diccionario **no significa que todas estén implementadas**.

| Código | Nombre | Familia | Estado de implementación a verificar |
|---|---|---|---|
| `CANT_ANIMALES_TOTAL` | Cantidad total de animales | Población | Verificar en repositorio |
| `CANT_ANIMALES_ACTIVOS` | Cantidad de animales activos | Población | Verificar en repositorio |
| `ANIMALES_POR_SEXO` | Distribución de animales por sexo | Población | Verificar en repositorio |
| `PESO_PROMEDIO_FINCA` | Peso promedio del rebaño | Peso | Verificar en repositorio |
| `PESO_TOTAL_FINCA` | Biomasa total en pie | Peso | Verificar en repositorio |
| `GMD_INDIVIDUAL` | Ganancia media diaria individual | Crecimiento | Verificar en repositorio; no asumir implementación |
| `SUP_TOTAL_POTREROS` | Superficie total de potreros | Territorial | Verificar en repositorio |
| `CARGA_ANIMAL_HA` | Carga animal por hectárea | Capacidad de carga | Verificar composición/implementación |

### Distinción crítica

El catálogo V1 es una **decisión de alcance**, no una declaración de que las ocho métricas ya estén construidas.

La implementación debe comprobarse contra el código real.

---

# 9. Contrato de comunicación para métricas

Cuando IA 1 describa una métrica debe usar, como mínimo:

```text
CODIGO:
NOMBRE:
FAMILIA:
FUENTE:
CAMPOS:
FILTROS:
OPERACION:
COMPOSICION:
UNIDAD:
TIPO_RESULTADO:
DATOS_FALTANTES:
VALIDACIONES:
ESTADO_REAL:
ARCHIVOS_RELACIONADOS:
PRUEBAS_EXISTENTES:
TRABAJO_PENDIENTE:
```

Si algún campo no aplica, debe escribir **N/A**, no inventar información.

---

# 10. Regla de evidencia

Toda afirmación técnica importante debe poder relacionarse con una de estas evidencias:

1. archivo y ruta del repositorio;
2. clase, función, modelo o configuración concreta;
3. prueba ejecutada;
4. contrato/documento previamente aprobado;
5. decisión explícita del proyecto.

Una explicación conceptual sin evidencia no debe clasificarse como implementación.

---

# 11. Protocolo de entrega de código

Cuando un nodo solicite implementación, IA 1 debe entregar:

1. **Resumen corto del cambio.**
2. **Archivos creados/modificados.**
3. **Código implementado.**
4. **Pruebas ejecutadas.**
5. **Resultado de las pruebas.**
6. **Limitaciones o pendientes reales.**
7. **Confirmación de si el nodo puede cerrarse.**

No sustituir estos elementos por una explicación teórica.

---

# 12. Protocolo ante contradicciones

Si IA 1 detecta una contradicción entre:

- código y documentación;
- documentación y modelo actual;
- catálogo y capacidad real del motor;
- contrato anterior y contrato vigente;

debe informar:

```text
CONTRADICCIÓN DETECTADA
Fuente A:
Fuente B:
Diferencia:
Impacto:
Nodo afectado:
Propuesta de resolución:
```

No debe corregir silenciosamente una decisión previamente cerrada.

---

# 13. Regla de continuidad entre sesiones e IAs

Una nueva IA debe poder comenzar su trabajo leyendo este documento y los documentos específicos del nodo correspondiente.

Por tanto:

- las definiciones no deben depender exclusivamente del contexto de una conversación;
- los nombres de modelos, métricas y operaciones deben mantenerse estables;
- los cambios de significado deben quedar registrados;
- el repositorio debe permitir reconstruir por qué una decisión existe.

---

# 14. Relación con la planificación de Fase 3

Este protocolo **no modifica ni reabre** los resultados de 3.1, 3.2 o 3.3.

Sirve como infraestructura de comunicación para los nodos siguientes.

Estado conocido al momento de establecer este protocolo:

- **3.1 — Modelo conceptual:** cerrado.
- **3.2 — Inventario histórico y estado real:** cerrado.
- **3.3 — Catálogo inicial de métricas:** cerrado.
- **3.4 — Especificación formal V1:** siguiente nodo de trabajo.

Si posteriormente aparece una incidencia, se actuará desde el nodo donde se detecte y se reabrirán nodos anteriores únicamente con evidencia técnica.

---

# 15. Regla final para IA 1

> **Trabaja sobre el nodo solicitado, usa este diccionario como lenguaje común, verifica el estado real en el repositorio y entrega exactamente el resultado pedido. No conviertas una tarea de análisis en literatura, ni una propuesta en implementación, ni un nodo cerrado en una nueva investigación sin causa técnica.**

---

**Documento:** `docs/AI1_COMMUNICATION_PROTOCOL.md`  
**Repositorio:** `hata1010/hato-ai-lab`  
**Uso:** referencia obligatoria para la comunicación técnica con IA 1 y para mantener continuidad entre sesiones.

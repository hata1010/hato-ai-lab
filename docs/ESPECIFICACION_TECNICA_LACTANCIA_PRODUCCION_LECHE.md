# Especificación técnica — Lactancia / Producción de leche

**Estado:** ESPECIFICACIÓN CONCLUIDA — NO IMPLEMENTADA

## 1. Objetivo

Diseñar la captura histórica de producción de leche necesaria para que Hato pueda calcular indicadores de lactancia de forma trazable, por animal, finca y periodo, sin inventar datos ni mezclar producción de animales o fincas.

La cadena será:

`CAPTURA DE ORDEÑO → REGISTRO HISTÓRICO → LACTACIÓN → MOTOR DE MÉTRICAS → INDICADORES → PANEL`

## 2. Principio de diseño

El módulo debe registrar observaciones reales y permitir derivar métricas. No debe guardar como dato primario un KPI que pueda calcularse a partir del historial.

Cada registro debe conservar como mínimo:
- animal;
- finca;
- fecha/hora o fecha del registro;
- cantidad de leche;
- unidad;
- turno/sesión de ordeño cuando aplique;
- método/origen del registro;
- usuario o dispositivo que lo registró;
- observaciones y trazabilidad.

## 3. Conceptos que deben quedar separados

### 3.1 Registro de producción
Es la observación de leche obtenida en un momento o sesión concreta.

### 3.2 Día de control / test day
Agrupa las observaciones necesarias para representar la producción diaria del animal según el método de registro adoptado.

### 3.3 Lactación
Periodo productivo asociado a una hembra después del parto y hasta el secado o terminación de la lactación.

### 3.4 Cierre de lactación
Estado histórico que permite distinguir una lactación en curso de una terminada y explicar por qué terminó.

## 4. Datos de captura propuestos

### Entidad: RegistroProduccionLeche

Campos conceptuales:
- animal;
- finca;
- fecha/hora;
- cantidad;
- unidad de medida;
- turno (mañana/tarde/noche, si aplica);
- método de medición (manual, medidor, sistema automático);
- dispositivo/equipo, si aplica;
- usuario responsable;
- origen del dato;
- observaciones.

### Entidad: Lactacion

Campos conceptuales:
- animal;
- número de lactación/paridad;
- parto de inicio;
- fecha de inicio;
- fecha de secado/fin, nullable mientras esté activa;
- estado (en curso, terminada, interrumpida);
- motivo de terminación;
- producción acumulada derivada o resumen materializado únicamente si existe una razón técnica para conservarlo;
- fuente/metodología de cálculo;
- auditoría.

La relación con reproducción es deliberada: el parto debe ser el evento que contextualiza el inicio de una lactación. No se debe duplicar la información reproductiva sin necesidad.

## 5. Composición de la leche

Debe dejarse preparado el diseño para resultados de análisis, sin obligar a que cada finca disponga de laboratorio.

Variables potenciales:
- grasa;
- proteína;
- lactosa;
- sólidos totales;
- células somáticas;
- urea u otros analitos cuando exista fuente válida.

Estos datos deben modelarse como observaciones de análisis vinculadas al registro de leche o al test day, no como valores inventados o calculados sin metodología.

## 6. Métricas que el módulo puede habilitar

### Básicas
- producción por ordeño;
- producción diaria;
- producción por animal;
- producción por finca;
- producción por periodo;
- promedio diario;
- días en leche (DIM).

### De lactación
- producción acumulada por lactación;
- duración de lactación;
- producción a 305 días cuando corresponda al método adoptado;
- producción por día de lactación;
- persistencia, cuando exista metodología y datos suficientes;
- comparación entre lactaciones del mismo animal.

### Composición
- porcentaje de grasa;
- porcentaje de proteína;
- relación producción/composición;
- tendencias de calidad.

## 7. 305 días: regla importante

Hato **no debe asumir que 305 días es una verdad universal**.

ICAR contempla procedimientos específicos para estimar producción de lactación y reconoce diferentes tipos de lactaciones, incluyendo lactaciones en curso, cortas, secas antes de tiempo y superiores a 305 días. Las reglas de extensión deben estar documentadas y justificadas. citeturn0search24turn0search26

FAO también documenta el uso de 305 días como referencia, pero advierte que su aplicación puede no ser adecuada de la misma manera en sistemas tropicales. citeturn0search0turn0search10

Por tanto, Hato debe guardar **metodología + versión + fuente** cuando produzca una métrica normalizada de 305 días.

## 8. Calidad y validación

El sistema debe detectar antes de aceptar o publicar datos:

- cantidad negativa;
- unidades incompatibles;
- duplicados del mismo evento;
- fecha imposible respecto al nacimiento/parto;
- registro fuera de una lactación válida;
- producción biológicamente improbable según límites configurables;
- animal inexistente o perteneciente a otra finca;
- discontinuidades sospechosas.

ICAR recomienda controles de plausibilidad, detección de valores atípicos e inconsistencias biológicas y documentación de los procedimientos de edición/calidad. citeturn0search3

## 9. Integración con reproducción

La lactancia debe consumir el contexto reproductivo, especialmente:

`Animal → Parto → Lactación → Registros de leche`

Esto evita duplicar fechas de parto y permite que futuras métricas relacionen producción con intervalo entre partos, días abiertos, paridad y estado reproductivo.

## 10. Integración con salud

Los eventos sanitarios deben permanecer en `EventoSalud` y relacionarse temporalmente con la lactación. Esto permitirá posteriormente estudiar, por ejemplo, incidencia de mastitis durante los días en leche, sin duplicar la historia clínica.

ICAR define indicadores sanitarios que pueden expresarse dentro de periodos de lactación, como la incidencia de mastitis clínica entre los días 1 y 305 en leche. citeturn0search28

## 11. Fuentes técnicas de referencia

- **ICAR — Dairy Cattle Milk Recording**, incluyendo procedimientos para producción de 24 horas y producción de lactación. citeturn0search25turn0search24
- **ICAR — Dairy Cattle Genetic Evaluation**, para reglas de tratamiento de lactaciones y control de calidad. citeturn0search3
- **FAO — Milk yield and lactation length in tropical cattle**, para contexto de duración de lactación y referencia de 305 días. citeturn0search0
- **FAO — Breeding plans for ruminant livestock in the tropics**, que muestra estructuras históricas de registros de vaca, producción, lactación, parto y composición. citeturn0search13

Estas fuentes son referencias de normalización. Hato no las convierte automáticamente en fórmulas oficiales: cada métrica debe tener definición, unidad, fuente, metodología y versión.

## 12. Reutilización de Hato

Antes de crear modelos nuevos debe reutilizarse:

- `Animal` para identidad y pertenencia;
- `Finca` para aislamiento multi-finca;
- `EventoSalud` para salud;
- módulo de reproducción para el parto una vez implementado;
- Motor de Métricas para fórmulas y definiciones;
- auditoría existente para trazabilidad.

## 13. Lo que NO se implementa en esta etapa

- No crear migraciones.
- No modificar modelos existentes.
- No alterar el Panel Operativo V2.
- No conectar APIs externas.
- No inventar valores productivos.
- No declarar métricas oficiales sin metodología validada.

## 14. Resultado esperado

Al finalizar la implementación futura, Hato deberá poder responder:

> ¿Cuánta leche produjo este animal, en qué ordeño, durante qué lactación, después de qué parto, en qué finca, con qué método de medición y de dónde salió el dato?

Y el Motor deberá poder transformar ese historial en métricas reproducibles y auditables.

## 15. Próximo paso

Después de validar esta especificación, realizar una comparación técnica contra los modelos actuales y la especificación de Reproducción. Solo después se diseñarán las migraciones y formularios necesarios.

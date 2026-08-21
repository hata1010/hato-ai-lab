# Métricas habilitadas — Reproducción y Lactancia

## 1. Propósito

Relacionar cada módulo de captura con las métricas que puede habilitar de forma trazable, sin convertir una métrica en un dato almacenado cuando puede derivarse del historial.

## 2. Reproducción

| Métrica | Datos mínimos | Unidad | Estado |
|---|---|---|---|
| Tasa de concepción | servicios + diagnósticos | % | Pendiente de definición formal de denominador |
| Tasa de preñez | diagnósticos/gestaciones | % | Pendiente de definición formal de población y ventana |
| Servicios por concepción | servicios + concepciones | servicios/concepción | Pendiente de definición formal |
| Días abiertos | parto + diagnóstico positivo posterior | días | 🟢 Integrada en Motor |
| Intervalo entre partos | partos sucesivos | días | 🟢 Integrada en Motor |
| Edad al primer servicio | nacimiento + primer servicio | días/años | Pendiente de integración |
| Edad al primer parto | nacimiento + primer parto | días/años | Pendiente de integración |
| Duración de gestación | servicio/concepción + parto | días | Pendiente de integración |

## 3. Lactancia

| Métrica | Datos mínimos | Unidad | Estado |
|---|---|---|---|
| Producción por control | ControlLeche | kg o L | Fuente disponible para derivación |
| Producción acumulada | controles de una lactación | kg o L | 🟢 Integrada en Motor |
| Producción por lactación | inicio/fin + controles | kg o L | Pendiente de metodología de agregación final |
| Duración de lactación | inicio + fin | días | 🟢 Integrada en Motor |
| Producción por día | producción + duración/intervalo | kg/día o L/día | Pendiente de integración |
| Producción estandarizada | historial suficiente + metodología aprobada | unidad definida | No implementar hasta aprobar estándar |
| Calidad/composición | grasa, proteína y otros controles | % / unidad específica | Pendiente de captura e integración |

## 4. Integración con el Motor de Métricas

Las funciones integradas se registran en el catálogo operativo del Motor y trabajan sobre los objetos históricos existentes:

- `IEP_ANIMAL`: toma los dos partos más recientes de la hembra.
- `DIAS_ABIERTOS_ANIMAL`: toma el último parto y el primer diagnóstico positivo posterior.
- `LECHE_ACUM_LACTANCIA`: suma controles de una lactancia solamente cuando toda la serie utiliza una misma unidad.
- `DURACION_LACTANCIA`: calcula días entre inicio y secado de una lactancia cerrada.

## 5. Reglas del Motor

- Las fórmulas pertenecen al Motor de Métricas, no a los modelos de captura.
- Cada fórmula debe tener versión, unidad, fuente, alcance y definición del denominador cuando corresponda.
- No calcular una métrica cuando falten los datos mínimos; usar `ErrorDatosInsuficientes`.
- No mezclar kg y L sin una conversión explícita y documentada.
- Toda métrica debe poder rastrearse hasta los registros que la originaron.
- Las métricas deben respetar finca, periodo y población seleccionada.
- Las tasas de concepción y preñez no se implementan todavía porque su población/denominador formal aún no está cerrado.

## 6. Estado

**INTEGRACIÓN PARCIAL CONCLUIDA — 4 MÉTRICAS CONECTADAS AL MOTOR.**

Las métricas que requieren una definición zootécnica adicional no se implementan por anticipado.

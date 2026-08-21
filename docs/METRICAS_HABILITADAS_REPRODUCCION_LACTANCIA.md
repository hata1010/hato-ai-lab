# Métricas habilitadas — Reproducción y Lactancia

## 1. Propósito

Relacionar cada módulo de captura con las métricas que puede habilitar de forma trazable, sin convertir una métrica en un dato almacenado cuando puede derivarse del historial.

## 2. Reproducción

| Métrica | Datos mínimos | Unidad | Observación |
|---|---|---|---|
| Tasa de concepción | servicios + diagnósticos | % | Debe definir población y periodo |
| Tasa de preñez | diagnósticos/gestaciones | % | Definir denominador y ventana |
| Servicios por concepción | servicios + concepciones | servicios/concepción | Solo con datos completos |
| Días abiertos | parto + nueva concepción/servicio | días | La fórmula depende de la definición adoptada |
| Intervalo entre partos | partos sucesivos | días | Requiere dos partos válidos |
| Edad al primer servicio | nacimiento + primer servicio | días/años | Requiere fecha de nacimiento |
| Edad al primer parto | nacimiento + primer parto | días/años | Requiere nacimiento y parto |
| Duración de gestación | servicio/concepción + parto | días | Requiere vínculo temporal confiable |

## 3. Lactancia

| Métrica | Datos mínimos | Unidad | Observación |
|---|---|---|---|
| Producción por control | ControlLeche | kg o L | Mantener unidad explícita |
| Producción acumulada | controles de una lactación | kg o L | Depende de cobertura de controles |
| Producción por lactación | inicio/fin + controles | kg o L | Requiere metodología de agregación |
| Duración de lactación | inicio + fin | días | Puede estar abierta |
| Producción por día | producción + duración/intervalo | kg/día o L/día | Definir denominador |
| Producción estandarizada | historial suficiente + metodología aprobada | unidad definida | No implementar fórmula hasta aprobar estándar |
| Calidad/composición | grasa, proteína y otros controles | % / unidad específica | Solo cuando exista captura suficiente |

## 4. Reglas del Motor de Métricas

- Las fórmulas pertenecen al Motor de Métricas, no a los modelos de captura.
- Cada fórmula debe tener versión, unidad, fuente, alcance y definición del denominador.
- No calcular una métrica cuando falten los datos mínimos; mostrar ausencia o insuficiencia de datos.
- No mezclar kg y L sin una conversión explícita y documentada.
- Toda métrica debe poder rastrearse hasta los registros que la originaron.
- Las métricas deben respetar finca, periodo y población seleccionada.

## 5. Estado

**DEFINICIÓN DE MÉTRICAS CONCLUIDA — NO IMPLEMENTADA.**

Este documento define qué puede habilitar cada módulo. No autoriza por sí mismo migraciones ni cambios en código.

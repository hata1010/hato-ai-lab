# Prompts por fase — Hato SDD

Este archivo reúne el contrato de prompts que proponemos para aplicar SDD en Hato. Se basa en el flujo ya utilizado durante el desarrollo y en las reglas de memoria, trazabilidad y validación del repositorio.

| Fase | Prompt esencial |
|---|---|
| Contexto | `Lee la memoria y documentación relevante del repositorio. Resume únicamente el contexto verificable necesario para esta tarea. Distingue hechos, inferencias y desconocidos. No modifiques código.` |
| Requerimiento | `Analiza el nuevo requerimiento. No escribas código. Identifica objetivo, actores, alcance, restricciones, dependencias y posibles conflictos con decisiones existentes. Espera aprobación.` |
| Spec | `NO escribas código. Genera una Spec con contexto, objetivo, actores, historias de usuario, RF numerados, requisitos no funcionales, casos límite, fuera de alcance, criterios de finalización y dudas abiertas. Relaciona cada requisito con evidencia o decisión existente cuando aplique.` |
| Clarificación | `Revisa la Spec como QA/arquitecto. Detecta ambigüedades, contradicciones, casos límite ausentes, riesgos y conflictos con memoria o decisiones. No resuelvas las dudas: enuméralas para aprobación humana.` |
| Plan | `Lee la memoria, decisiones y Spec aprobada. Sin código, genera un plan de implementación por módulos, archivos/componentes afectados, dependencias, estrategia de pruebas y riesgos. Indica qué RF cubre cada parte.` |
| Tasks | `Divide el plan en tareas pequeñas y verificables, ordenadas por dependencia. Cada tarea debe indicar alcance, archivos previstos, RF relacionados y una condición 'Hecho cuando'. No implementes.` |
| Implementación | `Implementa SOLO la tarea aprobada. No amplíes el alcance. Revisa primero el código existente. Ejecuta los tests pertinentes y reporta exactamente qué cambió y qué resultado obtuviste. PÁRATE al terminar.` |
| Validación | `Recorre la Spec requisito por requisito. Para cada RF indica evidencia de implementación, test asociado, resultado y validación manual necesaria. Veredicto final: SPEC CUMPLIDA / NO CUMPLIDA / PENDIENTE.` |
| Auditoría | `Audita la implementación contra la Spec, las decisiones y el estado del repositorio. No corrijas código. Presenta hallazgos con ruta, símbolo o evidencia reproducible y clasifica cada uno como HECHO, INFERENCIA, SUPUESTO o DESCONOCIDO.` |
| Cambio | `Nuevo requisito: <X>. NO toques código. Determina si requiere nueva Spec, revisión de una Spec existente o una decisión arquitectónica. Muestra primero el impacto y el cambio documental propuesto.` |
| Consolidación | `Consolida el resultado validado en la memoria del proyecto. Actualiza solo el conocimiento estructural que deba persistir. No conviertas la memoria en diario de conversación.` |

## Regla transversal

La IA no debe saltarse fases para acelerar una tarea cuando el cambio tenga impacto funcional o arquitectónico. El humano mantiene el criterio de aceptación y la aprobación de cambios importantes.

## Estado

Los prompts están definidos como contrato inicial. Todavía falta convertirlos en Skills reutilizables y automatizar el encadenamiento entre fases.

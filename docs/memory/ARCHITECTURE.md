# Hato AI Architect — Arquitectura de memoria

## Objetivo
Proporcionar a Hato una memoria persistente, estructurada y recuperable para mantener continuidad entre sesiones.

## Capas de memoria
1. **Memoria fundacional** — historia, arquitectura, decisiones y estado del proyecto.
2. **Memoria de sesión** — conocimiento relevante producido durante una sesión o hilo.
3. **MEMORY_CHECKPOINT** — punto de preservación del estado relevante cuando un hilo crece o antes de cambiar de hilo.
4. **Memoria diaria** — consolidación programada de cambios relevantes.

## Pipeline de consolidación
```text
Hilo de conversación
        ↓
Análisis de contenido
        ↓
Detección de relevancia para Hato
        ↓
Filtrado de contenido ajeno
        ↓
Clasificación
        ↓
Memoria estructurada
        ↓
Validación
        ↓
GitHub
```

## Clasificación mínima
- Historia
- Arquitectura
- Decisión
- Implementación
- Prueba / experimento
- Problema
- Solución
- Idea aprobada
- Estado actual
- Próximo paso

## Regla fundamental
Un hilo no equivale a memoria del proyecto. El sistema debe extraer conocimiento, no almacenar conversaciones indiscriminadamente.

## MEMORY_CHECKPOINT
`MEMORY_CHECKPOINT` es el mecanismo de preservación del estado cognitivo y técnico relevante de un hilo. Debe permitir guardar un punto seguro antes de que el contexto se vuelva crítico o antes de continuar en otro hilo.

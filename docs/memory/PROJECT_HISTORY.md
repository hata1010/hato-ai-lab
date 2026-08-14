# Hato AI Architect — Historia del proyecto

## Origen y propósito
Hato AI Architect se concibe como un laboratorio de desarrollo humano–IA orientado a construir un sistema capaz de colaborar en el desarrollo, documentar decisiones y conservar continuidad entre sesiones.

## Evolución documentada
- Se estableció `hata1010/hato-ai-lab` como repositorio del proyecto.
- Se creó y validó una GitHub App para que Hato AI Architect pueda operar sobre el repositorio mediante la API de GitHub.
- Se validó la obtención y uso del Installation Token.
- Se realizó una prueba real de escritura y creación de commit mediante la aplicación.
- Se decidió que GitHub será también un lugar persistente para la memoria estructurada del proyecto.
- Se creó `docs/memory/PROJECT_MEMORY.md` como semilla de la memoria persistente.
- Se definió la necesidad de una consolidación histórica de los hilos de trabajo.
- Se definió el concepto `MEMORY_CHECKPOINT` para preservar el estado relevante de un hilo antes de que el contexto se vuelva crítico.

## Principio de continuidad
La continuidad de Hato no debe depender exclusivamente de la permanencia de un hilo de conversación. El conocimiento relevante debe poder convertirse en memoria estructurada y persistirse en el repositorio.

## Criterio de consolidación
Los hilos pueden contener temas ajenos al proyecto. Por tanto, no se deben copiar conversaciones completas. El consolidador debe identificar, filtrar y clasificar únicamente el conocimiento útil para Hato.

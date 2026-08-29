# Spec HATO-SDD-001 — Ciclo controlado de evolución de Hato

## Contexto y objetivo
Hato necesita evolucionar con múltiples IAs y sesiones sin depender de la memoria de una conversación concreta. Esta Spec formaliza un ciclo de desarrollo basado en especificaciones, decisiones persistentes, implementación verificable y validación humana, utilizando el repositorio como fuente de verdad.

## Usuarios / actores
- **Humano responsable:** define intención, aprueba alcance y valida el resultado.
- **IA arquitecta/analista:** analiza contexto, requisitos, riesgos y diseño.
- **IA implementadora:** ejecuta únicamente tareas aprobadas.
- **IA crítica/auditora:** contrasta implementación, tests y evidencia contra la Spec.
- **Repositorio Git:** conserva memoria, decisiones, código, tests y trazabilidad.

## Historias de usuario
- H1: Como responsable del proyecto, quiero expresar un requisito como una Spec verificable para que la IA no tenga que interpretar indefinidamente mi intención.
- H2: Como responsable del proyecto, quiero revisar el plan antes de implementar para controlar el diseño generado por IA.
- H3: Como responsable del proyecto, quiero relacionar tareas y tests con requisitos para poder demostrar qué parte de la Spec está cumplida.
- H4: Como responsable del proyecto, quiero conservar decisiones y resultados en el repositorio para que otra IA pueda continuar el trabajo sin depender de la conversación anterior.
- H5: Como responsable del proyecto, quiero poder iterar una funcionalidad sin perder la trazabilidad de sus versiones anteriores.

## Requisitos funcionales (criterios de aceptación en EARS)
- RF-1: CUANDO se proponga una funcionalidad con impacto funcional, EL SISTEMA DE TRABAJO deberá permitir documentarla mediante una Spec antes de la implementación.
- RF-2: CUANDO exista una Spec, EL PROCESO deberá identificar actores, requisitos funcionales, casos límite, fuera de alcance y criterios de finalización.
- RF-3: CUANDO una Spec contenga ambigüedades o contradicciones, EL PROCESO deberá detectarlas durante la fase de clarificación antes de la implementación.
- RF-4: CUANDO una Spec sea aprobada, EL PROCESO deberá producir un plan y tareas trazables a sus requisitos.
- RF-5: CUANDO se implemente una tarea, LA IA deberá limitar los cambios al alcance aprobado y ejecutar las pruebas pertinentes.
- RF-6: CUANDO termine la implementación, EL PROCESO deberá contrastar cada requisito de la Spec con evidencia de código, tests y/o validación funcional.
- RF-7: SI un requisito no puede demostrarse, EL PROCESO deberá marcar la Spec como NO CUMPLIDA o PENDIENTE y no declararla terminada.
- RF-8: CUANDO aparezca un nuevo requisito, EL PROCESO deberá determinar si corresponde a una nueva Spec, una revisión de una Spec existente o una nueva decisión arquitectónica.
- RF-9: MIENTRAS una decisión arquitectónica siga vigente, LAS IAs deberán respetarla salvo aprobación explícita de un cambio.
- RF-10: EL REPOSITORIO deberá conservar la memoria estructural, decisiones y evidencia necesaria para continuar el desarrollo entre sesiones.

## Requisitos no funcionales
- Trazabilidad: requisitos, tareas, código, tests y validación deben poder relacionarse.
- Reproducibilidad: las comprobaciones importantes deben poder repetirse.
- Seguridad: ninguna IA debe asumir autorización para realizar cambios destructivos.
- Modularidad: la metodología no debe acoplarse innecesariamente al código Django.
- Continuidad: otra sesión o IA debe poder recuperar el contexto desde el repositorio.

## Casos límite
- Un requisito contradice una decisión arquitectónica existente.
- La Spec es demasiado ambigua para generar tareas verificables.
- Los tests pasan pero la funcionalidad no cumple la intención de la Spec.
- La implementación funciona pero modifica componentes fuera de alcance.
- Una IA no encuentra evidencia suficiente y confunde desconocimiento con inexistencia.
- Un cambio aparentemente pequeño requiere modificar una decisión arquitectónica.
- Una nueva iteración modifica una Spec ya validada.

## Fuera de alcance
- Automatizar completamente la toma de decisiones humanas.
- Permitir que una IA declare por sí sola que el producto completo está terminado.
- Introducir todavía Skills, subagentes o MCP como requisito técnico obligatorio.
- Sustituir Git por una memoria conversacional.
- Cambiar la arquitectura Django existente únicamente para implementar esta metodología.

## Criterios de finalización
- La metodología está documentada en el repositorio.
- Existe una Spec con requisitos verificables.
- Cada requisito tiene una estrategia de validación.
- El proceso contempla clarificación, plan, tasks, implementación y validación.
- La validación humana conserva la decisión final.
- Los cambios posteriores pueden iniciar una nueva iteración sin perder trazabilidad.

## Dudas abiertas
- [NECESITA ACLARACIÓN] Definir el identificador y ubicación oficial de las Specs futuras de Hato.
- [NECESITA ACLARACIÓN] Determinar cuándo una modificación requiere una nueva Spec frente a una revisión versionada.
- [NECESITA IMPLEMENTACIÓN] Convertir los prompts de `prompts.md` en Skills reutilizables.
- [NECESITA IMPLEMENTACIÓN] Definir automatización futura para validación y trazabilidad sin delegar el criterio humano.

## Relación con el estado actual
Esta Spec no pretende inventar una arquitectura nueva. Formaliza capacidades y reglas ya presentes en la memoria de Hato: repositorio como fuente de verdad, decisiones persistentes, checkpoints, trazabilidad, tests, validación y continuidad humano–IA.

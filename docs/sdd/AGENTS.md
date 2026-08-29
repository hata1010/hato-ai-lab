# AGENTS.md — Hato AI Lab / SDD

## Proyecto
Hato AI Lab es un laboratorio de desarrollo humano–IA cuyo proyecto principal es Hato, un sistema modular para gestión ganadera construido principalmente con Django/Python. El repositorio contiene código, memoria persistente, documentación, herramientas de continuidad, pruebas y decisiones arquitectónicas.

## Fuente de verdad
- El repositorio Git es la fuente de verdad del proyecto.
- La conversación con una IA es un medio de trabajo, no la memoria principal.
- Antes de modificar código, consultar el estado real del repositorio y la documentación relevante.
- No inventar contexto cuando exista incertidumbre: distinguir HECHO VERIFICADO, INFERENCIA, SUPUESTO y DESCONOCIDO POR FALTA DE EVIDENCIA.

## Contexto que debe leerse
Antes de una tarea relevante, consultar según corresponda:
- `memory/PROJECT_MEMORY.md`
- `memory/DECISIONS.md`
- `docs/memory/ARCHITECTURE.md`
- `docs/memory/CURRENT_STATE.md`
- la Spec activa y sus tareas, cuando existan
- el código y los tests afectados

## Arquitectura y reglas
- Mantener la arquitectura modular.
- No romper funcionalidades existentes.
- Separar datos, reglas de negocio e interfaz.
- El motor de métricas debe permanecer independiente del dashboard y de las vistas.
- La Finca es el tenant soberano de Hato V1 y `UsuarioFinca` representa la autorización y el rol.
- No introducir cambios arquitectónicos importantes sin registrar primero la decisión correspondiente.
- No usar `git push --force` ni reemplazar historia remota sin revisión explícita.
- No modificar partes no relacionadas con la tarea.

## Flujo SDD de Hato
1. Requerimiento
2. Spec
3. Clarificación
4. Plan
5. Tasks
6. Implementación
7. Tests
8. Validación humana
9. Evidencia
10. Consolidación
11. Iteración

La IA propone y ejecuta dentro del alcance aprobado; el humano conserva la decisión y la validación final.

## Comandos habituales
- Ejecutar servidor: `python manage.py runserver`
- Tests completos: `python manage.py test`
- Tests del módulo ganado: `python manage.py test apps.ganado`
- Comprobación Django: `python manage.py check`

## Al terminar una tarea
- Ejecutar los tests pertinentes.
- Ejecutar `python manage.py check` cuando el cambio afecte Django.
- Informar exactamente qué se modificó.
- Informar qué pruebas se ejecutaron y su resultado.
- Indicar cualquier validación manual pendiente.
- No declarar una Spec cumplida solo porque el código o los tests parezcan correctos: la validación debe contrastarse contra los requisitos de la Spec.

## Estado de madurez de esta metodología
Este archivo formaliza las reglas que ya existen en el proyecto. Todavía faltan automatizar de forma completa las fases de Spec, clarificación, plan, tasks y validación mediante Skills o herramientas equivalentes.

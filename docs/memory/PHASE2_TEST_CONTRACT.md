# Hato AI — Contrato de Pruebas de Fase 2 (2.11)

## Propósito

2.11 define la batería de pruebas que valida el pipeline de continuidad y sus contratos antes del E2E.

## Cobertura mínima

### Unitarias
- validación de contratos 2.3–2.10;
- tipos de conocimiento;
- destinos de memoria;
- comparación NEW/UPDATE/DUPLICATE/CONTRADICTION/OBSOLETE/REVIEW;
- resolución de conflictos;
- generación de propuestas;
- autorización y validación de persistencia;
- checkpoint posterior;
- eventos del Audit Trail.

### Integración
- 2.3 → 2.4;
- 2.4 → 2.5;
- 2.5 → 2.6;
- 2.6 → 2.7;
- 2.7 → 2.8;
- 2.8 → 2.9/2.10.

### Casos de conflicto
- contradicción directa;
- cambio de versión;
- conflicto temporal;
- conflicto de alcance;
- evidencia insuficiente;
- propuesta no aprobada;
- intento de modificar Memoria Fundacional sin autorización;
- fallo de persistencia sin cambios parciales.

## Criterios de aprobación

- los contratos rechazan entradas inválidas;
- no se pierde procedencia;
- no se borra historia;
- las propuestas no aprobadas no persisten;
- los conflictos no resueltos llegan a revisión;
- una consolidación válida puede producir checkpoint y auditoría coherentes;
- un fallo no deja estado parcial.

## Regla de cierre

**2.11 se considera cerrado a nivel de contrato cuando la matriz de pruebas y criterios de aceptación quedan formalizados.** La ejecución automática de la suite queda como implementación operativa posterior.

## Estado

**CERRADO — contrato de Pruebas de Fase 2 definido.**

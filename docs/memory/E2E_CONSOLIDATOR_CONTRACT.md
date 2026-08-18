# Hato AI — Contrato E2E del Consolidator (2.12)

## Propósito

2.12 define la prueba de extremo a extremo del flujo completo:

```text
Entrada
  ↓
Extracción
  ↓
Estructuración
  ↓
Clasificación
  ↓
Comparación
  ↓
Resolución
  ↓
Propuesta
  ↓
Persistencia
  ↓
Checkpoint
  ↓
Audit Trail
```

## Escenarios mínimos

1. **Conocimiento nuevo:** entra una decisión nueva y termina persistida con auditoría y checkpoint.
2. **Actualización:** conocimiento existente se amplía y conserva referencia histórica.
3. **Duplicado:** no crea una copia innecesaria.
4. **Contradicción:** se detecta, se resuelve o se escala a revisión sin borrar historia.
5. **Rechazo:** una propuesta no aprobada no modifica memoria.
6. **Fallo:** una falla intermedia no deja persistencia parcial.

## Invariantes E2E

- La procedencia se conserva desde la entrada hasta el resultado final.
- Toda escritura aprobada puede rastrearse mediante Audit Trail.
- Una consolidación válida genera un checkpoint posterior válido.
- La memoria histórica permanece disponible.
- La Memoria Fundacional no se modifica sin autorización explícita.
- El resultado final es reproducible a partir de las entradas y reglas del pipeline.

## Evidencias esperadas

El E2E debe producir:

- resultado de cada etapa;
- estado final de memoria;
- identificador de propuesta;
- resultado de persistencia;
- `audit_id`;
- `checkpoint_id`;
- resultado global `PASS` o `FAIL`;
- diagnóstico de la primera etapa que falle.

## Criterio de cierre

**2.12 se considera cerrado a nivel de contrato cuando los escenarios, invariantes y evidencias E2E están formalizados.** La ejecución automatizada real queda como implementación operativa posterior.

## Estado

**CERRADO — contrato E2E del Consolidator definido.**

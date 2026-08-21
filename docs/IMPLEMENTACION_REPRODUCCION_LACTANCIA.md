# Implementación — Reproducción y Lactancia

## Estado

**IMPLEMENTADA EN GITHUB — PENDIENTE DE APLICACIÓN Y VALIDACIÓN EN LA COPIA LOCAL.**

## Componentes

### Reproducción
- `EventoReproductivo`: servicio/monta, IA/IATF, diagnóstico de gestación, parto, aborto/pérdida y destete.
- `toro`: relación real con `Animal` para trazabilidad del progenitor masculino cuando corresponde.
- `semen_codigo`: identificación de pajilla/lote para IA/IATF.
- `CriaNacimiento`: vincula un parto con una cría `Animal` sin duplicar la genealogía existente.

### Lactancia
- `Lactancia`: ciclo productivo de una hembra.
- `parto_origen`: vínculo opcional con el parto que origina la lactancia.
- `ControlLeche`: registros por fecha, jornada, cantidad y unidad (`kg` o `L`).

## Reglas implementadas

- Reproducción y lactancia requieren animal hembra.
- Los registros nuevos deben pertenecer a la misma finca que el animal o evento relacionado.
- Toro debe ser macho, de la misma finca y especie.
- Monta natural requiere toro y no admite código de semen.
- IA/IATF requiere código de semen/pajilla.
- Diagnóstico requiere resultado de gestación.
- Parto requiere tipo de parto.
- Lactancia secada requiere fecha de secado.
- La fecha de secado no puede ser anterior al inicio.
- Una lactancia tiene número único por animal.
- Un control de leche no puede ser negativo o cero.
- Un control debe quedar dentro del periodo de su lactancia.
- No se almacena `dias_lactancia`; se deriva de las fechas.
- No se convierte automáticamente litros a kilogramos.
- Las métricas siguen perteneciendo al Motor de Métricas, no a los modelos de captura.

## Captura

Se añadieron registros administrativos para los cuatro modelos, con búsqueda, filtros, relaciones y campos de auditoría.

## Pruebas

Se incorporaron pruebas para las principales validaciones de reproducción, lactancia, cantidades y aislamiento por finca.

## Nota operativa

La migración `0002_reproduccion_lactancia.py` fue creada de acuerdo con el diseño aprobado. Debe ejecutarse en la copia local mediante Django antes de considerar la etapa completamente verificada.

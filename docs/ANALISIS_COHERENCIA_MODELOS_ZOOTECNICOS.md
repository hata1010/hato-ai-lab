# Análisis de coherencia — modelos actuales y captura zootécnica

**Estado:** ANÁLISIS CONCLUIDO — NO IMPLEMENTADO
**Fecha:** 2026-08-21

## 1. Alcance

Se comparó la arquitectura de captura zootécnica propuesta para Reproducción y Lactancia/Producción de leche contra los modelos actualmente presentes en `apps/ganado/models.py` de `main`.

La revisión se realizó contra el repositorio, no contra una copia local.

## 2. Resultado ejecutivo

**ESTATUS: 🟡 VIABLE CON AJUSTES**

La arquitectura actual tiene una base sólida para identidad animal, pertenencia multi-finca, genealogía, pesajes, salud, movimientos, genética y documentos. Sin embargo, no existe todavía una estructura específica para registrar el ciclo reproductivo ni la producción de leche histórica.

Por tanto, la propuesta es compatible con el sistema, pero requiere nuevos componentes antes de poder producir métricas reproductivas o de lactancia de forma auditable.

## 3. Lo que ya puede reutilizarse

### Animal

`Animal` ya proporciona identificación por arete, fecha de nacimiento, sexo, especie, raza declarada, finca, genealogía mediante `padre` y `madre`, estado y auditoría. Además, `clean()` valida sexo, especie y pertenencia de finca de padre y madre.

### PesajeAnimal

Existe historial de fecha/hora y peso en kg por animal. Puede reutilizarse para métricas reproductivas y productivas que necesiten edad o evolución corporal.

### EventoSalud

Existe un historial sanitario por animal con fecha/hora, tipo, producto/medicamento, dosis y veterinario. La lactancia debe relacionarse temporalmente con este historial en lugar de duplicar enfermedades o tratamientos.

### MovimientoAnimal

Existe historial de permanencia del animal en potreros y validación de pertenencia de finca. Puede aportar contexto espacial/productivo cuando una métrica lo requiera.

### ComposicionGenetica y documentos

Ya existen estructuras para composición genética y documentos de respaldo. No deben duplicarse en reproducción o lactancia.

## 4. Vacíos identificados

### Reproducción

Falta una entidad histórica para registrar explícitamente servicio/inseminación, diagnóstico de gestación, parto, pérdida reproductiva, aborto cuando aplique y destete cuando una métrica seleccionada lo necesite.

La genealogía existente identifica parentescos, pero no reemplaza el historial temporal de eventos reproductivos.

### Lactancia

Faltan estructuras para registro de producción de leche por ordeño/sesión, día de control, lactación asociada al parto, secado/fin de lactación y análisis de composición de leche cuando exista.

## 5. Relación correcta

`Animal → Eventos reproductivos → Parto → Lactación → Registros de leche`

En paralelo: `Animal → EventoSalud`.

La salud no debe copiarse dentro de Lactación. Se relacionará por animal y tiempo.

## 6. Multi-finca

La pertenencia a finca ya está presente en `Animal` y existen validaciones que impiden mezclar animales con padres/madres o potreros de otra finca. Las nuevas entidades deben mantener explícitamente esta frontera lógica.

## 7. Motor de Métricas

La arquitectura es compatible con el Motor porque los eventos y registros históricos pueden actuar como fuentes primarias y las métricas como derivaciones. No se debe guardar como dato primario un KPI que pueda calcularse desde el historial.

## 8. Compatibilidad con Lactancia

La especificación de lactancia es coherente con la arquitectura actual: reutiliza `Animal`, `EventoSalud` y el futuro módulo de reproducción, y no propone duplicar esos conceptos. La regla de 305 días debe permanecer metodológica y versionada.

## 9. Compatibilidad con Reproducción

La genealogía actual es un fundamento, pero no es un historial reproductivo. El futuro módulo debe complementar `Animal`, no sustituirlo.

## 10. Riesgos

1. Duplicar modelos o conceptos existentes.
2. Guardar KPIs como datos primarios.
3. Permitir registros entre fincas.
4. Asociar lactaciones sin contexto reproductivo válido.
5. Aplicar reglas de 305 días sin metodología y versión.
6. Mezclar datos manuales y automáticos sin conservar origen.
7. Construir el dashboard antes de disponer de captura histórica suficiente.

## 11. Orden recomendado

1. Especificación de Reproducción.
2. Especificación de Lactancia/Producción de leche.
3. Comparación y diseño definitivo de modelos.
4. Migraciones.
5. Formularios/admin/API de captura.
6. Pruebas de validación y aislamiento multi-finca.
7. Integración con Motor de Métricas.
8. Indicadores.
9. Panel Operativo V2.

## 12. Decisión

**VIABLE CON AJUSTES.** No existe bloqueo arquitectónico. La base actual puede sostener los módulos propuestos, pero faltan entidades históricas específicas para reproducción y producción de leche.

**No se modifica código en esta etapa.**

## 13. Siguiente etapa

Diseñar el modelo definitivo del módulo de Reproducción y compararlo con Lactancia antes de crear migraciones. La implementación debe comenzar únicamente después de cerrar esa revisión de coherencia.

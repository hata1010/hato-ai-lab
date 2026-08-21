# Inventario de datos existentes y faltantes — captura zootécnica

**Fecha:** 2026-08-21  
**Estado:** ANÁLISIS CONCLUIDO — PUBLICADO  
**Fuente de verificación:** `main` del repositorio `hata1010/hato-ai-lab`

## 1. Objetivo

Determinar qué datos de captura zootécnica ya existen en Hato y cuáles faltan para que Reproducción y Lactancia/Producción de leche puedan implementarse de forma histórica, auditable, multi-finca y compatible con el Motor de Métricas.

## 2. Datos que ya existen

### Identidad y contexto del animal

`Animal` ya captura:

- número de arete;
- nombre;
- fecha de nacimiento;
- sexo;
- especie;
- raza declarada;
- categoría;
- finca;
- microchip;
- tatuaje;
- registro genealógico;
- padre y madre;
- estado;
- observaciones;
- auditoría de creación y actualización.

Además, las validaciones comprueban sexo, especie y pertenencia de finca de padre y madre.

### Procedencia y adquisición

Existen `ProcedenciaAnimal`, `Adquisicion` y `AdquisicionAnimal`, con fecha, origen/proveedor, documento, costo y relación con finca.

### Genealogía y genética

Existe genealogía directa en `Animal` y `ComposicionGenetica` permite registrar raza, porcentaje, método, confiabilidad y fecha de verificación.

### Peso

`PesajeAnimal` conserva fecha/hora y peso en kg por animal, con índice por animal y fecha.

### Salud

`EventoSalud` conserva por animal fecha/hora, tipo de evento, producto/medicamento, dosis, veterinario y observaciones. Esto permite construir una historia sanitaria básica sin duplicarla en reproducción o lactancia.

### Movimientos y pastoreo

`MovimientoAnimal` conserva entrada/salida de potrero, estado activo, tipo de pasto y observaciones, con validación de pertenencia del potrero a la finca del animal.

### Documentación

`DocumentoAnimal` permite asociar documentos de pedigree, registro genealógico, ADN, sanitario, transporte y otros.

## 3. Datos que faltan

### A. Reproducción — faltantes principales

No existe todavía una entidad histórica específica para:

- servicio reproductivo;
- tipo de servicio (monta natural, inseminación u otros que se aprueben);
- toro/semental utilizado;
- inseminador o responsable;
- fecha del servicio;
- diagnóstico de gestación;
- resultado del diagnóstico;
- fecha del diagnóstico;
- parto como evento reproductivo histórico;
- tipo/resultado del parto;
- crías vinculadas al parto;
- aborto o pérdida reproductiva;
- causas/observaciones reproductivas;
- destete como evento cuando una métrica seleccionada lo requiera.

La genealogía `padre`/`madre` no sustituye estos eventos porque no conserva por sí sola la secuencia temporal del ciclo reproductivo.

### B. Lactancia — faltantes principales

No existe todavía una estructura histórica para:

- lactación individual asociada a un parto;
- fecha de inicio de lactación;
- fecha de secado/fin;
- número de lactación/paridad cuando corresponda;
- producción por ordeño o sesión;
- fecha/hora de cada registro de leche;
- unidad y método de medición;
- responsable/origen del dato;
- controles periódicos de producción;
- composición de leche cuando se disponga de ella;
- observaciones y calidad del registro.

### C. Datos transversales que deben quedar definidos

Antes de implementar, deben definirse de forma uniforme:

- origen del dato (manual, dispositivo, importación, integración externa, etc.);
- usuario/responsable de captura;
- fecha/hora efectiva del evento frente a fecha/hora de registro;
- unidad de medida;
- finca y animal como límites de seguridad;
- evidencia o documento asociado cuando aplique;
- correcciones históricas sin destruir el registro original.

## 4. Datos que NO debemos duplicar

No crear copias de:

- identidad del animal;
- padre/madre;
- finca;
- pesajes;
- eventos sanitarios;
- composición genética;
- documentos;
- movimientos de potrero.

Los nuevos módulos deben relacionarse con estas fuentes existentes.

## 5. Capacidad para métricas

La situación actual es:

**Animal + Pesajes + Salud + Movimientos + Genealogía = base disponible.**

**Reproducción histórica + Lactación + Registros de leche = captura pendiente.**

Por ello, el Motor de Métricas puede soportar las futuras fórmulas, pero las métricas reproductivas y de lactancia no deben declararse como disponibles hasta que existan los datos históricos necesarios.

## 6. Decisión

**ESTATUS: 🟡 VIABLE CON AJUSTES.**

No existe bloqueo arquitectónico. El trabajo pendiente es de captura histórica y modelado específico, no de reemplazar la arquitectura existente.

## 7. Próximo paso

Diseñar definitivamente los modelos de Reproducción y Lactancia en conjunto, incluyendo relaciones, cardinalidades, validaciones, origen del dato, aislamiento multi-finca y eventos históricos. Solo después se autorizarán migraciones e implementación.

**NO IMPLEMENTADO EN CÓDIGO.**

# Hato AI Lab — Inventario y Diseño de Captura Zootécnica

**Estado:** CONCLUIDO — DISEÑO PUBLICADO, IMPLEMENTACIÓN DE DATOS PENDIENTE  
**Fecha:** 2026-08-21  
**Etapa:** Preparación de Fase 6  
**Alcance:** Inventario del repositorio + diseño de captura histórica zootécnica. No se crean migraciones ni se altera código funcional en esta etapa.

## 1. Objetivo

Definir qué información debe capturar Hato para que sus métricas zootécnicas puedan calcularse a partir de datos históricos reales, trazables y acotados a la finca.

La relación adoptada es:

```text
CAPTURA → HISTORIA → MOTOR DE MÉTRICAS → INDICADORES → PANEL
```

Una métrica no se considera completa solamente porque el Motor pueda expresarla. También debe existir una fuente de datos suficiente para calcularla.

## 2. Estado verificado del repositorio

La arquitectura actual ya contiene una base importante de captura.

### 2.1 Core / finca

`apps/core/models.py` contiene:

- `Finca`, con ubicación geográfica `PointField` SRID 4326, superficie, zona horaria y pertenencia del registro.
- `Potrero`, con finca, ubicación, superficie, capacidad, carga, tipo/calidad de pasto, estado, fechas de pastoreo y `PolygonField` SRID 4326.
- `UsuarioFinca`, que mantiene la autorización por finca.

La finca sigue siendo la unidad empresarial/productiva y el contexto multi-finca no debe reconstruirse.

### 2.2 Ganado

`apps/ganado/models.py` ya contiene:

- `Animal`.
- `ProcedenciaAnimal`.
- `Adquisicion` / `AdquisicionAnimal`.
- `ComposicionGenetica`.
- `DocumentoAnimal`.
- `MovimientoAnimal`.
- `PesajeAnimal`.
- `EventoSalud`.

Esto significa que **no se debe crear desde cero un módulo de captura ganadera**.

### 2.3 Capturas que ya existen

#### Identidad e historial básico

`Animal` ya registra identificación, nacimiento, sexo, especie, raza, categoría, finca, microchip, tatuaje, genealogía, estado y auditoría.

#### Pesaje

`PesajeAnimal` ya conserva animal, fecha/hora, peso en kg y observaciones, con índice por animal/fecha.

Esto permite construir posteriormente métricas como peso promedio y GMD, siempre que exista una serie temporal suficiente.

#### Salud

`EventoSalud` ya contempla vacunación, desparasitación, enfermedad/diagnóstico, tratamiento, lesión, cirugía, examen, consulta y otros eventos. También posee producto/medicamento, dosis, veterinario, fecha y observaciones.

Esto constituye una base real para una historia sanitaria, pero **todavía no equivale a una historia clínica veterinaria completa**.

#### Movimientos y pastoreo

`MovimientoAnimal` conserva entrada/salida, potrero, estado, tipo de pasto y observaciones, con validación de finca.

Esto proporciona una base para historial de ocupación y rotación.

## 3. Vacíos de captura identificados

Los siguientes dominios no aparecen como modelos históricos específicos en el inventario verificado y deben diseñarse antes de depender de sus métricas.

### 3.1 Reproducción

Se requiere una estructura histórica explícita para, según corresponda al sistema productivo:

- servicio/monta/inseminación;
- fecha del servicio;
- toro/semental o material genético;
- diagnóstico de gestación;
- resultado de gestación;
- aborto/pérdida cuando aplique;
- parto;
- cría resultante;
- número de parto/paridad;
- eventos reproductivos relevantes.

Esto habilita métricas como tasa de preñez, tasa de nacimiento, intervalo entre partos y días abiertos.

### 3.2 Lactancia y producción de leche

Se requiere captura histórica por animal y fecha/período para:

- inicio de lactancia;
- fin de lactancia;
- producción de leche;
- unidad de medida;
- fecha/hora o período de registro;
- número de ordeños cuando sea relevante;
- calidad/composición cuando exista información suficiente;
- observaciones y fuente del registro.

ICAR establece que el registro de leche parte de identificación animal, fecha de parto, cantidad de leche y fecha/hora o período del registro, y posteriormente permite calcular rendimientos acumulados e índices. [ICAR — Section 02: Cattle Milk Recording](https://wiki.icar.org/index.php/Section_02_%E2%80%93_Cattle_Milk_Recording)

### 3.3 Historia clínica / sanitaria ampliada

`EventoSalud` ya es una base funcional, pero para una historia clínica robusta se debe evaluar separar o complementar:

- diagnóstico estructurado;
- motivo/consulta;
- signos/observaciones clínicas;
- tratamiento;
- medicamento;
- principio activo, si se decide modelarlo;
- dosis y unidad;
- vía de administración;
- duración;
- responsable;
- resultado/evolución;
- retiro/tiempo de espera cuando aplique;
- documentos o resultados de laboratorio.

No se debe duplicar `EventoSalud` sin necesidad. Primero se debe determinar qué campos pueden evolucionar dentro del modelo existente y qué información necesita entidad propia.

### 3.4 Nacimientos y mortalidad

`Animal.fecha_nacimiento`, `ProcedenciaAnimal` y `Animal.estado` aportan información, pero no sustituyen necesariamente un historial de eventos.

Para indicadores temporales y auditoría se debe evaluar un registro explícito de:

- nacimiento;
- muerte;
- causa de muerte;
- fecha del evento;
- responsable/observaciones;
- vínculo con madre/cría cuando corresponda.

### 3.5 Crecimiento y destete

El pesaje ya existe. Falta determinar si se requiere registrar explícitamente:

- destete;
- fecha de destete;
- peso al destete;
- método/condición del pesaje;
- responsable.

El peso al destete no debe inferirse arbitrariamente a partir del pesaje más cercano si la definición oficial de Hato requiere un evento de destete.

### 3.6 Potrero y pastoreo

La geometría y el movimiento ya existen. Para métricas avanzadas de pastoreo conviene evaluar captura histórica de:

- entrada/salida por lote o grupo, además del animal individual cuando el manejo lo requiera;
- condición/altura/biomasa del pasto, si se desea calcular utilización real;
- disponibilidad de forraje;
- capacidad objetivo y metodología;
- eventos de manejo del potrero;
- lluvia u otras variables externas, únicamente si una métrica las necesita.

No se debe introducir una métrica de capacidad de pastoreo que requiera variables que Hato todavía no capture.

## 4. Catálogo inicial de métricas vinculadas a captura

| Métrica candidata | Captura principal | Estado de datos | Próximo paso |
|---|---|---|---|
| Peso promedio | `PesajeAnimal` | 🟢 Existe | Formalizar definición |
| GMD | `PesajeAnimal` + fechas | 🟡 Existe base | Formalizar fórmula y reglas de selección |
| Peso al nacimiento | `Animal` + evento/nacimiento + pesaje | 🟡 Parcial | Definir evento/pesaje válido |
| Peso al destete | Pesaje + evento destete | 🟡 Parcial | Diseñar captura de destete |
| Tasa de nacimiento | Reproducción + nacimientos | 🔴 Falta estructura específica | Diseñar reproducción |
| Mortalidad de terneros | Nacimiento + muerte | 🟡 Parcial | Diseñar evento de muerte y reglas |
| Intervalo entre partos | Partos | 🔴 Falta | Diseñar reproducción |
| Días abiertos | Parto + servicio/gestación | 🔴 Falta | Diseñar reproducción |
| Edad al primer servicio | Nacimiento + servicio | 🔴 Falta | Diseñar reproducción |
| Edad al primer parto | Nacimiento + parto | 🔴 Falta | Diseñar reproducción |
| Duración de lactancia | Parto + lactancia | 🔴 Falta | Diseñar lactancia |
| Leche/vaca/día | Lactancia | 🔴 Falta | Diseñar producción de leche |
| Leche/ha | Lactancia + superficie | 🔴 Falta | Diseñar lactancia y validar metodología |
| Kg carne/ha | Movimientos + pesos + eventos productivos | 🟡 Parcial | Formalizar definición y fuentes |
| Carga UGG/ha | Animal/peso + superficie + coeficientes | 🟡 Parcial | Validar metodología; no asumir 450 kg universal |
| Indicadores sanitarios | `EventoSalud` | 🟢 Base existente | Formalizar catálogo y reglas |

## 5. Fuentes de conocimiento utilizadas para orientar el diseño

Las fuentes externas se clasifican como conocimiento de referencia, no como código que Hato deba consumir obligatoriamente.

### FAO / FAOSTAT

FAOSTAT documenta indicadores de unidades ganaderas (LSU) y señala que los coeficientes se calculan por tipo de ganado y país. Por tanto, **Hato no debe convertir automáticamente `peso / 450` en una definición universal de UGG/ha sin validar la metodología seleccionada**.

Fuente: https://data.fao.org/catalog/dataset/16d3a7af-3704-414d-bf83-d3a32146ab83

### ICAR

ICAR mantiene guías internacionales para identificación y registro de animales, producción lechera, bovinos de carne, reproducción/fertilidad, genética y otros procesos de registro. La guía de leche confirma que los datos de captura deben permitir posteriormente calcular parámetros e índices.

Fuentes:
- https://wiki.icar.org/index.php/Guidelines
- https://wiki.icar.org/index.php/Section_02_%E2%80%93_Cattle_Milk_Recording

### Ciencia Agropecuaria

El artículo de De León-García et al. (2025) presenta un conjunto de índices zootécnicos e indicadores de productividad para sistemas doble propósito: tasa de nacimiento, mortalidad de terneros, intervalo entre partos, días abiertos, edad al primer servicio, edad al primer parto, duración de lactancia, pesos, producción de leche y carne por animal/año/ha, entre otros.

Debe utilizarse como **fuente científica de descubrimiento y comparación**, no como fórmula universal para todos los sistemas de Hato.

Fuente: https://www.revistacienciaagropecuaria.ac.pa/index.php/ciencia-agropecuaria/article/view/679

### AGROVOC

AGROVOC puede utilizarse como referencia terminológica para normalizar nombres y conceptos del dominio agropecuario. No sustituye la definición metodológica de una métrica.

## 6. Diseño de captura propuesto

La captura debe conservar la historia y no sobrescribir hechos anteriores.

```text
FINCA
  │
  └── ANIMAL
       │
       ├── Identificación / genealogía
       ├── Procedencia
       ├── Pesajes ───────────────► GMD / peso / crecimiento
       ├── Reproducción ──────────► preñez / parto / IEP / DA
       ├── Lactancias ────────────► leche / lactancia / productividad
       ├── Salud ─────────────────► eventos sanitarios / tratamientos
       ├── Nacimientos / muertes ─► demografía / mortalidad
       ├── Movimientos ───────────► pastoreo / permanencia
       └── Genética / documentos

FINCA
  │
  └── POTRERO
       ├── geometría
       ├── superficie
       ├── pasto
       ├── manejo
       └── historial de ocupación
```

Cada registro histórico debe conservar como mínimo, cuando sea aplicable:

- finca/contexto;
- entidad afectada;
- fecha/hora;
- valor y unidad;
- origen del dato;
- responsable/usuario cuando sea pertinente;
- observaciones;
- vínculo con eventos relacionados.

## 7. Relación con el Motor de Métricas

El Motor ya posee un modelo declarativo de `Metrica` y `VariableMetrica`, incluyendo categoría, periodicidad, tipo de resultado, fórmula, versión, fuente y campo. Esto es compatible conceptualmente con el diseño de captura: las métricas deben declarar de dónde proceden sus variables y no esconder su procedencia dentro de la interfaz.

El flujo objetivo queda:

```text
DATOS HISTÓRICOS
      ↓
FUENTES / CAMPOS
      ↓
VARIABLES DE MÉTRICA
      ↓
FÓRMULA / COMPOSICIÓN
      ↓
VALIDACIÓN
      ↓
RESULTADO + UNIDAD + PERÍODO + FINCA + TRAZABILIDAD
```

## 8. Reglas de diseño

1. No inventar datos para completar una métrica.
2. No declarar una métrica oficial sin definición formal y fuente documentada.
3. No asumir una fórmula universal cuando una fuente demuestra dependencia por país, especie, sistema o metodología.
4. No duplicar modelos existentes sin justificar la separación.
5. Mantener la finca como ámbito operativo y de autorización.
6. Mantener historial: los nuevos eventos no deben destruir el estado histórico.
7. Separar captura, cálculo y presentación.
8. El Panel consume resultados; no debe convertirse en el lugar donde se define la zootecnia.
9. Las fuentes externas sirven para investigación/normalización y, cuando proceda, para consumo de datos; no se convierten automáticamente en dependencias del núcleo Hato.
10. Cada métrica debe poder explicar qué datos utilizó, de qué finca, período y entidades provienen y qué versión de definición fue aplicada.

## 9. Estatus de esta etapa

**🟢 CONCLUIDO — INVENTARIO Y DISEÑO PUBLICADOS.**

**NO SE HAN CREADO MIGRACIONES NI SE HAN MODIFICADO LOS MODELOS FUNCIONALES EN ESTA ETAPA.**

### Resultado

- La base de captura ganadera existente es mayor de lo que parecía inicialmente.
- Pesajes, salud, movimientos, procedencia, genética y documentos ya tienen representación.
- Los vacíos estructurales principales están en reproducción, lactancia/producción de leche y ciertos eventos históricos productivos/sanitarios que requieren mayor granularidad.
- El Motor puede vincularse con estas fuentes mediante variables declarativas.
- El siguiente trabajo debe ser **diseño técnico de los módulos faltantes**, empezando por reproducción y lactancia, sin romper los modelos existentes.

## 10. Próximo paso

Antes de implementar modelos nuevos, realizar una especificación técnica por módulo:

1. Reproducción.
2. Lactancia/producción de leche.
3. Historia clínica sanitaria ampliada.
4. Eventos de nacimiento/muerte/destete.
5. Evolución del historial de pastoreo cuando las métricas seleccionadas lo requieran.

Cada especificación deberá identificar modelos, relaciones, reglas de validación, permisos por rol/finca, migraciones, formularios, pruebas y métricas habilitadas.

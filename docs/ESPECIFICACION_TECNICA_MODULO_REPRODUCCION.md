# Hato AI Lab — Especificación técnica: Módulo de Reproducción

**Estado:** CONCLUIDO — ESPECIFICACIÓN PUBLICADA, IMPLEMENTACIÓN PENDIENTE  
**Fecha:** 2026-08-21  
**Etapa:** Diseño previo a implementación  
**Alcance:** Definir el dominio de reproducción que Hato debe capturar y conservar históricamente para habilitar métricas reproductivas trazables. No se crean migraciones ni se modifica código funcional en esta etapa.

## 1. Objetivo

Construir una base de captura reproductiva por animal que permita registrar hechos históricos y posteriormente calcular métricas mediante el Motor de Métricas, sin poner la lógica zootécnica dentro del dashboard.

Cadena: `CAPTURA → HISTORIA → VARIABLES → MOTOR DE MÉTRICAS → INDICADORES → PANEL`.

El módulo debe servir para reproducción natural, inseminación artificial y, cuando corresponda, transferencia de embriones.

## 2. Fundamento técnico

ICAR recomienda registrar para reproducción el identificador del animal, fecha, persona que registra, finca/ubicación, código del evento reproductivo y animales relacionados. Contempla monta, inseminación, transferencia de embriones, parto, diagnóstico de gestación y resultados de cada servicio. ICAR también documenta intervalos como parto–primer servicio, días abiertos, intervalo entre servicios, intervalo entre partos y duración de gestación. 

FAO identifica como medidas fundamentales edad al primer parto, intervalo entre partos, tasas de fertilidad/concepción y servicios por concepción.

Estas fuentes son referencia metodológica. No se copia una fórmula al Motor solo porque aparezca en una fuente: cada métrica Hato deberá definir población, denominador, período, unidad, reglas de datos y fuente.

## 3. Relación con modelos existentes

`Animal` ya contiene identidad, sexo, nacimiento, especie, raza, finca y genealogía. `PesajeAnimal`, `EventoSalud`, `MovimientoAnimal`, procedencia, adquisiciones y genética ya proporcionan otros segmentos de la historia.

Reproducción debe complementar `Animal`, no reconstruirlo. La finca continúa siendo ámbito empresarial y de autorización.

## 4. Eventos reproductivos mínimos

### 4.1 Servicio reproductivo

Debe distinguir monta natural, inseminación artificial y servicio dirigido cuando el manejo lo requiera.

Datos: hembra, fecha/hora, tipo, semental cuando aplique, material genético cuando aplique, responsable, finca/contexto, observaciones y número/rango de servicio cuando sea necesario.

Para monta natural grupal debe poder registrarse período de exposición y posibles toros.

### 4.2 Diagnóstico de gestación

Datos: hembra, fecha, resultado (gestante/no gestante/indeterminado), método, responsable, servicio evaluado si se conoce y observaciones.

No se debe convertir un diagnóstico en una fecha de concepción exacta cuando la evidencia solo permite un intervalo.

### 4.3 Parto

Datos: madre, fecha/hora, número de parto/paridad, resultado, facilidad, número de crías, sexo e identificación de cada cría cuando exista, padre cuando sea conocido, tipo de nacimiento cuando aplique y observaciones.

Las crías deben vincularse a `Animal` y conservar genealogía.

### 4.4 Pérdida reproductiva

Debe permitir aborto, pérdida embrionaria/fetal u otro resultado adverso, con fecha/intervalo, tipo, gestación/servicio relacionado cuando sea conocido, causa/diagnóstico, responsable y observaciones.

No debe confundirse automáticamente con `EventoSalud`.

### 4.5 Transferencia de embriones

Cuando se soporte: madre genética, madre receptora, padre/genética del embrión, fecha, procedimiento, resultado y parto resultante. Debe conservarse la diferencia entre madre genética y receptora.

## 5. Modelo conceptual

```text
Animal
  ├── ServicioReproductivo
  │     ├── tipo / fecha
  │     ├── semental / material genético
  │     └── finca / responsable
  ├── DiagnosticoGestacion
  │     ├── fecha / método / resultado
  │     └── servicio relacionado
  ├── PerdidaReproductiva
  │     ├── fecha / tipo / causa
  │     └── servicio o gestación relacionada
  └── Parto
        ├── fecha / paridad / facilidad
        └── Crías → Animal
```

Este esquema es un contrato de dominio, no una orden de crear exactamente cuatro tablas. La implementación final debe revisar si algunas entidades pueden consolidarse sin perder trazabilidad.

## 6. Reglas de integridad

1. La hembra debe existir y pertenecer al contexto válido.
2. No se permiten relaciones consigo misma como padre/madre/semental.
3. Las fechas reproductivas deben respetar coherencia temporal básica.
4. Un diagnóstico puede quedar sin servicio relacionado si el registro histórico no permite determinarlo.
5. Un parto debe poder relacionarse con madre y, cuando exista evidencia, padre.
6. Las crías deben conservar vínculos genealógicos existentes.
7. Transferencia de embriones diferencia genética y receptora.
8. Los hechos históricos no se sobrescriben; las correcciones deben ser auditables.
9. Se conserva finca y responsable cuando corresponda.
10. No se exige información que el sistema productivo real no pueda capturar.

## 7. Métricas habilitadas

### Directas

- servicios por hembra;
- edad al primer servicio;
- intervalo entre servicios;
- edad al primer parto;
- intervalo entre partos;
- duración de gestación cuando la concepción esté suficientemente determinada;
- días abiertos cuando existan parto y concepción/servicio válidos.

### Tasas

- tasa de concepción;
- tasa de preñez;
- tasa de parto;
- tasa de nacimiento;
- servicios por concepción.

La definición debe fijar denominador, población elegible, ventana y tratamiento de casos sin diagnóstico.

### Gestión

Podrán derivarse hembras aptas para servicio, servidas en período, pendientes de diagnóstico, con días abiertos sobre un umbral definido y desempeño por finca/lote/raza/semental/período, solo cuando haya datos suficientes.

## 8. Qué no hacer

- No calcular preñez como gestantes actuales / total de hembras.
- No inferir concepción exacta si solo existe una ventana.
- No tratar todo servicio como inseminación.
- No atribuir una cría a un toro si hubo exposición a múltiples sementales sin evidencia suficiente.
- No usar `Animal.estado` como sustituto de eventos reproductivos.
- No poner fórmulas reproductivas en templates.
- No duplicar genealogía existente sin justificación.

## 9. Trazabilidad

Cada evento debe responder: **qué animal, qué ocurrió, cuándo, dónde, quién lo registró, con qué evidencia y con qué eventos se relaciona**.

Una métrica reproductiva debe poder remontarse a sus diagnósticos, servicios y animales/finca de origen.

## 10. Integración con Motor de Métricas

El Motor debe consumir variables de los eventos y no depender de la interfaz. Cada métrica deberá declarar nombre, definición, fórmula/algoritmo, unidad, población, período, fuente, versión, tratamiento de faltantes, ámbito y nivel de trazabilidad.

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

## 11. Dependencias

| Dependencia | Uso |
|---|---|
| `Animal` | identidad, sexo, nacimiento, genealogía, finca |
| `Finca` / `UsuarioFinca` | ámbito y autorización |
| `EventoSalud` | problemas reproductivos y tratamientos relacionados |
| `PesajeAnimal` | análisis condicionado por peso |
| `ComposicionGenetica` | análisis por genética |
| `DocumentoAnimal` | evidencias |
| Motor de Métricas | cálculo declarativo/versionado |
| Panel Operativo V2 | presentación, no definición |

## 12. Fuentes de referencia

- ICAR — Beef Cattle Recording: https://wiki.icar.org/index.php/Section_03%3A_Beef_Cattle_Recording
- ICAR — Female Fertility Guidelines: https://www.icar.org/wp-content/uploads/2016/12/Guidelines-for-female-fertility-in-dairy-cattle.pdf
- FAO — Measures of reproductive performance: https://www.fao.org/4/x5442e/x5442e06.htm
- FAO — Cattle reproductive performance: https://www.fao.org/4/x5522e/x5522e09.htm

## 13. Estatus

**🟢 CONCLUIDO — ESPECIFICACIÓN TÉCNICA PUBLICADA.**

**NO IMPLEMENTADO. NO HAY MIGRACIONES.**

Siguiente etapa: revisar esta especificación contra los modelos Django actuales y definir la implementación mínima necesaria. Solo después se crearán migraciones, formularios y pruebas.

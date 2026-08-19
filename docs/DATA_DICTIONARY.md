# Diccionario de Datos — Hato

**Versión:** 1.0  
**Estado:** Vigente  
**Fecha:** 2026-08-19  
**Propósito:** referencia semántica y técnica de los datos persistidos por Hato.

## 1. Propósito y alcance

Este documento **no es una base de datos**. Es el diccionario de datos del sistema: documenta qué entidades y campos existen, qué representan, cómo se relacionan y para qué se utilizan.

La estructura debe mantenerse alineada con los modelos Django reales del repositorio. La definición estructural de cada campo tiene como fuente primaria el modelo; este documento agrega su significado operativo y reglas de uso.

En esta versión se documentan los modelos persistentes de:

- `apps.core.models`
- `apps.ganado.models`
- `apps.produccion.models`

No se documentan aquí tablas internas de Django ni modelos de aplicaciones que no sean parte del dominio Hato.

## 2. Convenciones

| Término | Significado |
|---|---|
| PK | Clave primaria del registro. Normalmente `id`. |
| FK | Clave foránea hacia otra entidad. |
| O2O | Relación uno a uno. |
| `null=True` | La base de datos permite NULL. |
| `blank=True` | El campo puede quedar vacío en validaciones/formularios Django. |
| SRID 4326 | Sistema de referencia geográfica usado por los campos GIS de entrada. |
| ha | Hectáreas. |
| kg | Kilogramos. |
|

## 3. Reglas generales

1. **No inventar campos:** antes de construir consultas, métricas o código que use datos del sistema, consultar este diccionario y el modelo Django correspondiente.
2. **No confundir nombre con semántica:** un campo debe utilizarse según su significado documentado, no solamente por su nombre.
3. **Relaciones por FK:** cuando un dato pertenece a una finca, debe respetarse la relación empresarial definida por el modelo.
4. **Datos GIS:** `poligono` es la geometría del potrero; `area_hectareas` es un valor derivado que el modelo recalcula al guardar cuando existe geometría.
5. **Métricas:** una métrica debe declarar claramente fuente, campo, unidad, filtros y reglas de cálculo.
6. **Unidades:** los cálculos deben conservar las unidades documentadas y no mezclar magnitudes sin conversión explícita.

---

# 4. Aplicación `core`

## 4.1 Finca

Unidad empresarial principal. Los datos operativos pertenecen directa o indirectamente a una finca.

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador único | PK |
| `nombre` | CharField(200) | No / No | Nombre de la finca | Identificación |
| `nit` | CharField(50) | Sí / Sí | Identificación tributaria | Identificación empresarial |
| `direccion` | TextField | No / Sí | Dirección física | Información de finca |
| `telefono` | CharField(20) | No / Sí | Teléfono | Contacto |
| `email` | EmailField | No / Sí | Correo electrónico | Contacto |
| `ubicacion` | PointField SRID 4326 | Sí / Sí | Punto geográfico de la finca | Mapa/localización |
| `area_total` | DecimalField(10,2) | Sí / Sí | Área total declarada de la finca | Información territorial |
| `fecha_fundacion` | DateField | Sí / Sí | Fecha de fundación | Historial |
| `zona_horaria` | CharField(50) | No / No | Zona horaria operativa | Fechas y horarios |
| `moneda` | CharField(3) | No / No | Moneda de operación | Datos económicos |
| `is_active` | BooleanField | No / No | Indica si la finca está activa | Filtros operativos |
| `descripcion` | TextField | No / Sí | Descripción general | Información contextual |
| `created_at` | DateTimeField | — | Fecha de creación | Auditoría |
| `updated_at` | DateTimeField | — | Última actualización | Auditoría |
| `created_by` | FK User | Sí / Sí | Usuario que creó la finca | Auditoría |

## 4.2 Potrero

Espacio físico perteneciente exclusivamente a una finca.

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador único | PK |
| `finca` | FK Finca | No / No | Finca propietaria | Pertenencia |
| `nombre` | CharField(100) | No / No | Nombre del potrero | Identificación |
| `codigo` | CharField(20) | No / No | Código del potrero, único por finca | Identificación |
| `tipo` | CharField(20) | No / No | Tipo: potrero, corral, encierro, embarcadero u otro | Clasificación |
| `ubicacion` | PointField SRID 4326 | Sí / Sí | Punto de ubicación | Mapa |
| `area_hectareas` | DecimalField(10,2) | Sí / Sí | Área del espacio en hectáreas | Indicadores territoriales |
| `capacidad_animales` | IntegerField | Sí / Sí | Capacidad declarada de animales | Manejo |
| `carga_actual` | IntegerField | No / No | Cantidad actual registrada para el potrero | Manejo |
| `tipo_pasto` | CharField(100) | No / Sí | Tipo de pasto | Alimentación |
| `calidad_pasto` | CharField(20) | No / No | Calidad: excelente, bueno, regular o malo | Alimentación |
| `estado` | CharField(20) | No / No | Estado operativo del potrero | Manejo |
| `dias_descanso` | IntegerField | No / No | Días de descanso | Rotación |
| `fecha_ultimo_pastoreo` | DateField | Sí / Sí | Fecha del último pastoreo | Rotación |
| `poligono` | PolygonField SRID 4326 | Sí / Sí | Geometría espacial del potrero | Mapa y cálculo de superficie |
| `descripcion` | TextField | No / Sí | Descripción adicional | Contexto |
| `is_active` | BooleanField | No / No | Indica si el potrero está activo | Filtros |
| `created_at` | DateTimeField | — | Fecha de creación | Auditoría |
| `updated_at` | DateTimeField | — | Última actualización | Auditoría |

**Regla de superficie:** al guardar un `Potrero` con `poligono`, el modelo transforma la geometría a EPSG:3857, calcula el área en m² y guarda `area_hectareas = área_m² / 10.000`, redondeada a 2 decimales. Por tanto, `area_hectareas` es un dato derivado de `poligono`, no una geometría independiente.

---

# 5. Aplicación `ganado`

## 5.1 Especie

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `nombre` | CharField(50) | No / No | Nombre de la especie | Catálogo |
| `descripcion` | TextField | No / Sí | Descripción | Catálogo |

## 5.2 Raza

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `nombre` | CharField(100) | No / No | Nombre de la raza | Catálogo |
| `especie` | FK Especie | No / No | Especie a la que pertenece | Clasificación |
| `descripcion` | TextField | No / Sí | Descripción | Catálogo |

Regla: `nombre` es único dentro de una especie.

## 5.3 TipoPasto

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `nombre` | CharField(100) | No / No | Nombre del tipo de pasto | Catálogo |
| `descripcion` | TextField | No / Sí | Descripción | Catálogo |

## 5.4 Animal

Entidad central del inventario ganadero.

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `numero_arete` | CharField(50) | No / No | Identificador del arete | Identificación |
| `nombre_propio` | CharField(100) | No / Sí | Nombre del animal | Identificación |
| `fecha_nacimiento` | DateField | Sí / Sí | Fecha de nacimiento | Edad |
| `sexo` | CharField(1) | No / No | `M` macho, `H` hembra | Clasificación |
| `especie` | FK Especie | No / No | Especie del animal | Clasificación |
| `raza_declarada` | FK Raza | Sí / Sí | Raza declarada | Genética/clasificación |
| `categoria` | CharField(100) | No / Sí | Categoría productiva | Clasificación |
| `finca` | FK Finca | Sí / Sí | Finca a la que pertenece | Pertenencia empresarial |
| `microchip` | CharField(100) | No / Sí | Identificación electrónica | Identificación |
| `tatuaje` | CharField(100) | No / Sí | Identificación por tatuaje | Identificación |
| `registro_genealogico` | CharField(150) | No / Sí | Registro genealógico | Genealogía |
| `padre` | FK self | Sí / Sí | Animal padre | Genealogía |
| `madre` | FK self | Sí / Sí | Animal madre | Genealogía |
| `estado` | CharField(20) | No / No | Estado: activo, vendido, muerto, descartado o trasladado | Inventario/indicadores |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |
| `is_active` | BooleanField | No / No | Estado técnico del registro | Control |
| `created_at` | DateTimeField | — | Fecha de creación | Auditoría |
| `updated_at` | DateTimeField | — | Última actualización | Auditoría |

Reglas principales: `numero_arete` es único por finca; padre debe ser macho, madre debe ser hembra; padres deben corresponder a la misma especie y finca; padre y madre no pueden ser el mismo animal.

## 5.5 ProcedenciaAnimal

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `animal` | O2O Animal | No / No | Animal al que corresponde | Relación |
| `tipo` | CharField(30) | No / No | Nacimiento, compra, donación, traslado, intercambio u otro | Procedencia |
| `fecha` | DateField | Sí / Sí | Fecha de procedencia | Historial |
| `origen_nombre` | CharField(200) | No / Sí | Nombre del origen | Procedencia |
| `origen_identificacion` | CharField(150) | No / Sí | Identificación del origen | Procedencia |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

## 5.6 Adquisicion

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `finca` | FK Finca | No / No | Finca de la adquisición | Pertenencia |
| `proveedor` | CharField(200) | No / No | Proveedor | Adquisiciones |
| `fecha` | DateField | No / No | Fecha | Adquisiciones |
| `numero_documento` | CharField(100) | No / Sí | Factura/documento | Trazabilidad |
| `costo_total` | DecimalField(14,2) | Sí / Sí | Costo total | Economía |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

## 5.7 AdquisicionAnimal

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `adquisicion` | FK Adquisicion | No / No | Adquisición asociada | Relación |
| `animal` | O2O Animal | No / No | Animal adquirido | Relación |
| `precio_individual` | DecimalField(14,2) | Sí / Sí | Precio individual | Economía |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

Regla: el animal debe pertenecer a la misma finca de la adquisición.

## 5.8 ComposicionGenetica

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `animal` | FK Animal | No / No | Animal | Genética |
| `raza` | FK Raza | No / No | Raza componente | Genética |
| `porcentaje` | DecimalField(5,2) | No / No | Porcentaje de composición | Genética |
| `metodo` | CharField(30) | No / No | Pedigree, registro, ADN, declaración o estimación | Trazabilidad |
| `confiabilidad` | CharField(20) | No / No | Nivel de confiabilidad | Calidad del dato |
| `fecha_verificacion` | DateField | Sí / Sí | Fecha de verificación | Trazabilidad |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

Reglas: porcentaje entre 0 y 100; la raza debe pertenecer a la misma especie del animal.

## 5.9 DocumentoAnimal

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `animal` | FK Animal | No / No | Animal documentado | Relación |
| `tipo` | CharField(40) | No / No | Tipo de documento | Clasificación |
| `numero_documento` | CharField(150) | No / Sí | Número o referencia | Trazabilidad |
| `archivo` | FileField | Sí / Sí | Archivo asociado | Documentación |
| `fecha_documento` | DateField | Sí / Sí | Fecha del documento | Trazabilidad |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

## 5.10 MovimientoAnimal

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `animal` | FK Animal | No / No | Animal movilizado | Movimiento |
| `potrero` | FK Potrero | No / No | Potrero destino | Ubicación |
| `fecha_entrada` | DateTimeField | No / No | Entrada al potrero | Historial |
| `fecha_salida` | DateTimeField | Sí / Sí | Salida del potrero | Historial |
| `activo` | BooleanField | No / No | Indica movimiento vigente | Ubicación actual |
| `tipo_pasto` | FK TipoPasto | Sí / Sí | Tipo de pasto asociado | Alimentación |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

Reglas: solo un movimiento activo por animal; salida no puede ser anterior a entrada; movimiento activo no debe tener fecha de salida; animal y potrero deben pertenecer a la misma finca.

## 5.11 PesajeAnimal

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `animal` | FK Animal | No / No | Animal pesado | Relación |
| `fecha` | DateTimeField | No / No | Fecha y hora del pesaje | Historial |
| `peso_kg` | DecimalField(7,2) | No / No | Peso en kilogramos | Producción |
| `observaciones` | TextField | No / Sí | Observaciones | Contexto |

## 5.12 EventoSalud

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `animal` | FK Animal | No / No | Animal afectado | Salud |
| `tipo` | CharField(30) | No / No | Vacunación, desparasitación, enfermedad, tratamiento, lesión, cirugía, examen, consulta u otro | Salud |
| `fecha` | DateTimeField | No / No | Fecha y hora | Historial |
| `producto` | CharField(100) | No / Sí | Producto/medicamento | Tratamiento |
| `dosis` | CharField(50) | No / Sí | Dosis registrada | Tratamiento |
| `nombre_veterinario` | CharField(200) | No / Sí | Veterinario responsable | Trazabilidad |
| `observaciones` | TextField | No / Sí | Observaciones | Salud |

---

# 6. Aplicación `produccion`

## 6.1 Metrica

Define una métrica productiva y su fórmula, clasificación y ciclo de vida.

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `finca` | FK Finca | Sí / Sí | Finca propietaria de la definición; NULL permite métrica general | Alcance |
| `nombre` | CharField(200) | No / No | Nombre legible | Identidad |
| `codigo` | CharField(50) | No / No | Identificador usado por el motor | Ejecución |
| `descripcion` | TextField | No / Sí | Descripción | Documentación |
| `categoria` | CharField(30) | No / No | Categoría productiva | Clasificación |
| `unidad_resultado` | CharField(50) | No / Sí | Unidad del resultado | Interpretación |
| `periodicidad` | CharField(20) | No / No | Diaria, semanal, mensual, trimestral, semestral, anual o variable | Planificación |
| `tipo_resultado` | CharField(20) | No / No | Número, cantidad, peso, porcentaje, volumen, moneda, índice o booleano | Tipo de salida |
| `formula` | TextField | No / Sí | Expresión de cálculo | Motor de métricas |
| `activa` | BooleanField | No / No | Métrica habilitada | Control |
| `version` | PositiveIntegerField | No / No | Versión de definición | Evolución |
| `created_at` | DateTimeField | — | Fecha de creación | Auditoría |
| `updated_at` | DateTimeField | — | Última actualización | Auditoría |

Reglas: `codigo` y `nombre` son únicos por finca; una métrica puede ser global cuando `finca` es NULL.

## 6.2 VariableMetrica

Define las variables que alimentan una métrica.

| Campo | Tipo | Nulo/Vacío | Descripción | Uso |
|---|---|---|---|---|
| `id` | BigAutoField | — | Identificador | PK |
| `metrica` | FK Metrica | No / No | Métrica propietaria | Relación |
| `nombre` | CharField(100) | No / No | Nombre legible | Documentación |
| `codigo` | CharField(50) | No / No | Identificador utilizado en la fórmula | Motor |
| `tipo` | CharField(20) | No / No | Dato, calculada o parámetro | Clasificación |
| `fuente` | CharField(100) | No / Sí | Modelo/fuente de donde se obtiene | Origen |
| `campo` | CharField(100) | No / Sí | Campo de la fuente | Origen |
| `regla` | CharField(30) | No / No | Directo, primero, último, promedio, suma, mínimo, máximo o diferencia de fechas | Obtención |
| `orden` | PositiveIntegerField | No / No | Orden de la variable | Ejecución |
| `activa` | BooleanField | No / No | Variable habilitada | Control |

Regla: `codigo` es único dentro de una métrica.

---

# 7. Relaciones principales

```text
Finca
 ├── Potrero
 ├── Animal
 ├── Adquisicion
 └── Metrica

Animal
 ├── Especie → Raza
 ├── padre / madre → Animal
 ├── ProcedenciaAnimal
 ├── AdquisicionAnimal
 ├── ComposicionGenetica → Raza
 ├── DocumentoAnimal
 ├── MovimientoAnimal → Potrero
 ├── PesajeAnimal
 └── EventoSalud

Metrica
 └── VariableMetrica
```

# 8. Datos derivados y métricas

## Superficie de potreros

`Potrero.poligono` es la fuente geométrica. `Potrero.area_hectareas` es el valor derivado almacenado por el modelo. La métrica `SUP_TOTAL_POTREROS` debe documentar explícitamente si suma `area_hectareas` o si recalcula desde geometrías.

**Regla de diagnóstico:** antes de modificar el motor ante un resultado inesperado, comparar el valor almacenado con el área derivada directamente de `poligono`.

## Animales activos

`Animal.estado = "activo"` es el criterio de estado usado por las métricas actuales para identificar animales activos. `is_active` es un control técnico del registro y no debe confundirse automáticamente con `estado`.

## Peso actual

Las métricas de peso actuales utilizan el concepto de `PESO_ACTUAL`; la fuente histórica de pesos es `PesajeAnimal.peso_kg`. La definición exacta de "actual" debe permanecer en el motor/función correspondiente y no inferirse solamente del último campo visto.

# 9. Regla para futuras IAs

Antes de crear o modificar una métrica, consulta obligatoriamente:

1. este diccionario;
2. el modelo Django fuente;
3. las pruebas existentes de la métrica;
4. las reglas de negocio documentadas.

Si existe contradicción entre documentación y código, **no inventar una interpretación**: señalar la discrepancia y corregir primero la fuente correspondiente.

# 10. Mantenimiento

Este documento debe actualizarse cuando se agregue, elimine, renombre o cambie semánticamente un campo persistente del dominio. Las modificaciones deben publicarse junto con el cambio de modelo o como una actualización documental explícita.

**Fuente estructural de esta versión:** modelos Django del repositorio Hato AI Lab, rama `main`, consultados el 2026-08-19.
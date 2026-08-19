# PROJECT MEMORY
# HATO-AI-LAB

## 1. IDENTIDAD DEL PROYECTO

Nombre:
Hato AI Lab

Tipo:
Laboratorio de desarrollo humano–IA.

Propósito:
Construcción experimental de sistemas inteligentes orientados a
dominios concretos, combinando conocimiento humano, software,
modelado de dominio e inteligencia artificial.

---

## 2. VISIÓN

Construir sistemas donde el conocimiento del dominio pueda
representarse de forma estructurada y posteriormente ser utilizado
por motores de reglas, métricas, composición y razonamiento.

El objetivo no es solamente desarrollar una aplicación,
sino construir una arquitectura reutilizable para crear
sistemas inteligentes especializados.

---

## 3. PROYECTO ACTUAL

Proyecto principal:
Sistema inteligente para gestión ganadera.

Dominio inicial:
Gestión y producción ganadera.

Tecnología principal:
Django / Python.

Arquitectura:
Modular.

---

## 4. MOTOR DE MÉTRICAS

El proyecto incorpora un motor de métricas orientado al dominio.

Concepto fundamental:

Las métricas no deben estar codificadas únicamente como consultas
aisladas dentro de las vistas de una aplicación.

Deben poder definirse, componerse, validarse y ejecutarse mediante
una estructura declarativa.

El motor busca funcionar como un lenguaje específico del dominio
(DSL) orientado a métricas.

---

## 5. CONCEPTOS DEL MOTOR

Conceptos actualmente identificados:

- Métrica
- Datos de entrada
- Dimensiones
- Filtros
- Composición
- Validación
- Ejecución
- Resultado
- Trazabilidad

Ejemplo conceptual:

Datos
   ↓
MAPEAR
   ↓
FILTRAR
   ↓
AGREGAR
   ↓
CALCULAR
   ↓
VALIDAR
   ↓
RESULTADO

---

## 6. ARQUITECTURA ACTUAL

Aplicaciones principales:

apps/
├── core
├── ganado
├── mapas
└── administrador

Componentes principales:

core:
    entidades generales de la finca, contexto de tenant,
    membresías y autorización por finca.

ganado:
    animales, movimientos, pesajes, salud,
    adquisiciones y genética.

mapas:
    información geográfica y representación
    de fincas y potreros.

administrador:
    interfaz administrativa y dashboard.

---

## 7. DOMINIO GANADERO

Entidades principales:

- Finca
- Potrero
- Animal
- MovimientoAnimal
- PesajeAnimal
- EventoSalud
- Adquisicion
- AdquisicionAnimal
- DocumentoAnimal
- ComposicionGenetica
- ProcedenciaAnimal
- UsuarioFinca

---

## 8. INDICADORES

El sistema contempla indicadores relacionados con:

- población ganadera;
- peso promedio;
- evolución de peso;
- producción;
- salud;
- potreros;
- adquisiciones;
- producción de carne;
- producción de leche;
- indicadores mensuales;
- indicadores anuales.

---

## 9. PRINCIPIOS DE DESARROLLO

1. Modularidad.
2. Separación de responsabilidades.
3. No romper funcionalidades existentes.
4. Reutilización.
5. Trazabilidad.
6. Datos separados de reglas.
7. Métricas independientes de la interfaz.
8. Arquitectura preparada para crecimiento.
9. Documentar las decisiones importantes.
10. Construir primero el núcleo conceptual y después ampliar.

---

## 10. ESTADO ACTUAL

Actualmente existe una base funcional del sistema ganadero.

Se dispone de:

- estructura Django;
- modelo de finca;
- modelo ganadero;
- manejo de potreros;
- información geográfica;
- administración;
- dashboard;
- indicadores;
- datos de prueba;
- primeras implementaciones del motor de métricas;
- aislamiento Multi-Finca V1 y control de acceso por membresía.

El motor de métricas se encuentra en evolución.

---

## 11. TRABAJO EN CURSO

Prioridad actual:

Desarrollar y consolidar el motor de métricas como componente
independiente y reutilizable.

Objetivo inmediato:

Definir claramente su lenguaje, estructura, composición,
validación y ejecución antes de ampliar innecesariamente
la plataforma.

---

## 12. DECISIONES IMPORTANTES

- Mantener arquitectura modular.
- Evitar mezclar la lógica del motor con las vistas.
- Mantener el motor independiente del dashboard.
- No incorporar sensores físicos todavía.
- Mantener preparada la arquitectura para futuras extensiones.
- Documentar la evolución del proyecto.

---

## 13. FUTURO

Posibles extensiones:

- producción ganadera avanzada;
- inventario;
- insumos;
- compras;
- gastos;
- ingresos;
- inteligencia artificial;
- generación automática de componentes;
- nuevos dominios especializados;
- reutilización del motor fuera del dominio ganadero.

---

## 14. REGLA PARA ACTUALIZAR ESTA MEMORIA

Este archivo debe actualizarse únicamente cuando exista una
decisión, descubrimiento, cambio arquitectónico o avance importante
que deba conservarse para futuras sesiones.

No utilizarlo como diario de conversación.

La memoria debe conservar el conocimiento estructural del proyecto,
no cada detalle temporal del desarrollo.

---

## 15. PROTOCOLO DE CONTINUIDAD Y COORDINACIÓN HUMANO–IA

El proyecto ha identificado una necesidad operativa crítica:
la memoria persistente debe evitar que el trabajo dependa de la
continuidad de una conversación concreta.

Principios establecidos:

1. El repositorio es la fuente de verdad del proyecto; la conversación
   es un medio de trabajo, no la memoria principal.
2. Cuando exista incertidumbre sobre una decisión anterior, se debe
   consultar primero la memoria y el estado real del repositorio,
   antes de inferir o inventar contexto.
3. Cada componente de trabajo debe manejarse con estados verificables:
   EN CONSTRUCCIÓN → EN PRUEBA → CERRADO.
4. Una tarea que requiera participación humana debe indicar de forma
   explícita: qué ejecutar, dónde ejecutarlo, qué resultado se espera
   y qué evidencia debe devolverse para cerrar la tarea.
5. No se debe pedir al desarrollador que espere indefinidamente sin
   una razón técnica concreta. Si su participación es necesaria, debe
   solicitarse en el momento en que desbloquea el trabajo.
6. Las decisiones arquitectónicas importantes deben persistirse en
   memoria antes de ejecutar cambios potencialmente destructivos.
7. No usar `git push --force` ni reemplazar historias remotas sin
   comprobar primero la historia y la estructura existentes.
8. La integración del código Hato con Hato AI Lab debe conservar la
   memoria, documentación, herramientas y automatización existentes.
9. El código Django de Hato pertenece conceptualmente al laboratorio,
   dentro del área destinada al código, separado de memoria,
   documentación, herramientas y automatización.
10. La consolidación de sesiones es parte funcional del sistema de
    memoria, no una actividad opcional.

Este protocolo surge de la experiencia operativa del 2026-08-18 y
queda establecido como criterio para las siguientes sesiones.

---

## 16. CONCLUSIONES DEL EXPERIMENTO ENGINE + GMD + AUDITORÍA IA

Fecha: 2026-08-18
Estado: CERRADO COMO ETAPA EXPERIMENTAL

Durante la etapa se realizó una revisión del motor de métricas y se
consultaron dos IAs sobre cómo construir la métrica Ganancia Media
Diaria (GMD) utilizando la arquitectura existente.

### 16.1 Hallazgo principal sobre el Engine

El proyecto no debe entenderse como un catálogo terminado de métricas
individuales. El activo arquitectónico principal es el mecanismo que
permite construir métricas mediante funciones de dominio y composición.

Se identifican como piezas relevantes del Engine:

- funciones de dominio;
- `FuncionBase`;
- `Compositor`;
- `PlanMetrica`;
- `Mapear` y funciones de agregación;
- evaluador AST seguro con `Decimal`;
- mecanismo de explicación de la composición;
- interfaz HTML temporal utilizada como laboratorio para probar
  composiciones del motor.

Por tanto, una métrica como GMD debe utilizar primero las capacidades
existentes del Engine. No se debe crear prematuramente una función
monolítica que oculte las capacidades que ya posee el motor.

### 16.2 GMD: estado y siguiente objetivo

La métrica Ganancia Media Diaria (GMD) todavía NO está formalizada como
métrica terminada.

El siguiente objetivo técnico es construir GMD como caso de prueba
real del Engine, partiendo de las funcionalidades existentes.

La secuencia esperada es:

Pesajes
  ↓
funciones de dominio existentes
  ↓
composición
  ↓
PlanMetrica
  ↓
ejecución
  ↓
explicación
  ↓
resultado GMD

Solo si el Engine no dispone de una operación necesaria se deberá
identificar y diseñar esa nueva capacidad de forma explícita.

La interfaz HTML temporal debe recuperarse como laboratorio de prueba
antes de modificar el dashboard definitivo.

### 16.3 Resultado del contraste entre dos IAs

Las dos IAs produjeron diagnósticos diferentes sobre la arquitectura.
Una pudo identificar componentes concretos del Engine y detectar una
incompatibilidad real de interoperabilidad (`Mapear` utiliza la clave
`funcion`, no `funcion_elemento`), además de distinguir entre el
contrato conceptual de métricas y la implementación de `PlanMetrica`.

La segunda IA trabajó con una visión más limitada del repositorio y
concluyó que varios componentes no existían. Este resultado no debe
interpretarse automáticamente como que la arquitectura no existe:
representa una limitación de evidencia disponible para esa IA.

Conclusión metodológica:

Las auditorías realizadas por IA deben distinguir explícitamente entre:

- HECHO VERIFICADO;
- INFERENCIA;
- SUPUESTO;
- DESCONOCIDO POR FALTA DE EVIDENCIA.

Una futura auditoría automática del proyecto deberá proporcionar, cuando
sea posible, evidencia reproducible: ruta de archivo, símbolo encontrado,
commit/ref y resultado de la comprobación.

### 16.4 Visión futura de auditoría autónoma

Se establece como línea futura que el propio sistema Hato AI Lab pueda
analizar su repositorio y señalar:

- inconsistencias entre código y contratos;
- fallas detectables;
- pruebas faltantes;
- automatizaciones potencialmente útiles;
- discrepancias entre el estado documentado y el estado real.

El principio de seguridad para esta capacidad será inicialmente:

LEER → COMPARAR → DETECTAR → EXPLICAR → PROPONER → ESPERAR APROBACIÓN
HUMANA.

La modificación automática del código podrá evaluarse posteriormente,
cuando exista suficiente evidencia y control.

### 16.5 Cierre de la etapa

Esta etapa queda cerrada sin implementar todavía GMD.

No se considera un fracaso: el experimento permitió validar que el
Engine existente puede ser analizado como arquitectura de composición,
identificar puntos de interoperabilidad y definir una metodología más
rigurosa para evaluar IAs sobre el repositorio.

Próxima etapa:
recuperar el estado real del Engine y del HTML temporal de pruebas,
y construir GMD utilizando primero las funciones existentes.

---

## 17. MULTI-FINCA Y CONTROL DE ACCESO — HATO V1

Fecha: 2026-08-19
Estado: IMPLEMENTADO, PROBADO Y VERIFICADO

Se implementó el aislamiento de tenant y control de acceso por finca.
La Finca se mantiene como la unidad empresarial/productiva soberana y
no se introduce una entidad `Empresa` artificial.

### 17.1 Modelo de autorización

Se creó `UsuarioFinca`, que representa la membresía de un usuario en una
finca concreta y constituye el límite de autorización de Hato V1.

Roles definidos:

- propietario
- administrador
- operador
- veterinario
- auditor

La membresía contiene `activa`, permitiendo revocar acceso sin eliminar
el historial.

Existe una restricción única por pareja `usuario + finca` y dos índices
compuestos para consultas por usuario/estado y finca/estado.

### 17.2 Contexto de tenant

Se creó `apps/core/tenant.py` como módulo desacoplado para:

- obtener las fincas autorizadas de un usuario;
- verificar acceso a una finca concreta;
- obtener el rol del usuario dentro de una finca;
- resolver la finca activa desde la sesión;
- cambiar la finca activa mediante validación estricta.

La finca activa se conserva en `request.session['finca_activa_id']`.
El sistema ya no depende de parámetros inseguros como `?finca=102` para
resolver el ámbito operativo.

Los usuarios normales solo pueden seleccionar fincas con membresía activa.
La revocación de `activa` bloquea el acceso en la siguiente petición.

### 17.3 Root / Superusuario

`is_superuser=True` conserva alcance global sobre las fincas activas,
sin requerir una membresía `UsuarioFinca`.

Root puede operar globalmente y, cuando necesita un contexto concreto,
fijar una finca activa en sesión para trabajar o auditar mapas, potreros,
animales e indicadores dentro de ese ámbito.

### 17.4 Integración en vistas

Se protegieron las vistas sensibles mediante `verificar_acceso_finca`.

En `apps/core/views.py`:

- `seleccionar_finca` funciona exclusivamente mediante POST;
- `mapa_finca` valida autorización antes de entregar datos geográficos;
- `animales_por_potrero` valida autorización antes de consultar animales.

Las vistas administrativas y de producción resuelven el contexto desde
la finca activa y el conjunto de fincas autorizadas del usuario, evitando
el bypass mediante parámetros GET.

### 17.5 Migración de datos existente

`0006_usuariofinca.py` crea el esquema de membresías.

`0007_migrar_membresias_iniciales.py` realiza una migración de datos no
destructiva: para cada finca con `created_by`, crea o recupera una
membresía con rol `propietario` y `activa=True`.

No se inventan usuarios ni se eliminan fincas existentes. Las fincas sin
`created_by` quedan disponibles para asignación posterior por Root.

### 17.6 Seguridad verificada

Se creó `apps/core/test_security_tenant.py` con 10 pruebas automatizadas
que cubren:

1. aislamiento Finca A → Finca B;
2. protección contra manipulación de `?finca=`;
3. rechazo de selección POST no autorizada;
4. bloqueo por membresía inactiva;
5. usuario con múltiples fincas;
6. cambio de rol según finca;
7. acceso global de Root;
8. modo global de Root;
9. contexto operativo de Root;
10. preservación de autoría y membresía inicial.

Resultado reproducible reportado:
`python3 -m unittest apps.core.test_security_tenant -v`
→ **10/10 tests PASSED**.

### 17.7 Verificación global reportada

Al cierre de esta etapa se reportó:

- Seguridad Tenant: 10/10 PASSED;
- Motor de Métricas V1: 13/13 PASSED;
- Herramientas y Continuidad: 38/38 PASSED;
- Total global: **61/61 tests PASSED**;
- `integrity_check.py`: **PASS**.

Este resultado queda registrado como evidencia reportada del estado del
repositorio al 2026-08-19.

### 17.8 Decisiones derivadas

- La Finca es el tenant soberano de Hato V1.
- La autorización se modela explícitamente mediante `UsuarioFinca`.
- La selección de finca operativa ocurre mediante sesión y POST validado.
- La seguridad debe verificarse contra membresías activas en servidor.
- Root mantiene alcance global, con capacidad de fijar un contexto de finca.
- Los catálogos `Especie`, `Raza` y `TipoPasto` permanecen globales y no
  reciben `finca_id` en esta etapa.
- Se prioriza la separación entre identidad (`User`), autorización
  (`UsuarioFinca`) y ámbito de datos (`Finca`).

### 17.9 Estado de la etapa

**CERRADA:** Multi-Finca + Control de Acceso Hato V1.

El siguiente trabajo debe partir de este estado y no reconstruir el modelo
de tenant desde cero. Cualquier modificación futura de seguridad deberá
preservar las pruebas de aislamiento y la evidencia reproducible.

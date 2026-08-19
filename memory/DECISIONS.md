# DECISIONS

Registro de decisiones arquitectónicas y conceptuales
del proyecto Hato AI Lab.

---

## DEC-001 — Arquitectura modular

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

El proyecto utilizará una arquitectura modular, separando
las responsabilidades del sistema en componentes independientes.

### Motivo

Evitar que toda la lógica del sistema termine concentrada
en una única aplicación.

### Aplicación

La arquitectura contempla componentes como:

- core
- ganado
- mapas
- administrador
- motor de métricas

### Consecuencia

Los módulos deberán mantener responsabilidades claras
y comunicarse mediante interfaces bien definidas.

---

## DEC-002 — Motor de métricas independiente

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

El motor de métricas será tratado como un componente
independiente de la interfaz web.

### Motivo

Una métrica no debe depender de una página específica,
un dashboard o una vista de Django.

La misma métrica debe poder utilizarse desde diferentes
interfaces o sistemas.

### Consecuencia

La lógica de cálculo deberá permanecer separada de:

- templates;
- HTML;
- dashboard;
- vistas;
- componentes visuales.

---

## DEC-003 — Métricas como lenguaje específico de dominio

**Fecha:** 2026-08-13  
**Estado:** En desarrollo

### Decisión

El motor de métricas evolucionará hacia un lenguaje
específico de dominio (DSL) para expresar métricas.

### Motivo

Una métrica debe poder describirse mediante conceptos
del dominio en lugar de depender exclusivamente de
consultas SQL o código procedural.

### Concepto

Una definición conceptual puede representar:

DATOS
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

### Consecuencia

El lenguaje deberá permitir definir métricas de manera
declarativa y reproducible.

---

## DEC-004 — Separación entre datos y reglas

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

Los datos del dominio y las reglas de cálculo deberán
mantenerse conceptualmente separados.

### Motivo

Permitir que una misma regla pueda utilizarse sobre
diferentes conjuntos de datos.

### Consecuencia

Las reglas podrán evolucionar sin modificar
innecesariamente las estructuras de almacenamiento.

---

## DEC-005 — No incorporar sensores todavía

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

La primera versión del sistema no incorporará
hardware ni sensores físicos.

### Motivo

Primero se consolidará el modelo de información,
la arquitectura y el motor de métricas.

### Futuro

La arquitectura podrá incorporar posteriormente:

RFID
ESP32
LoRa
GPS
Gateways
Sensores

sin que estos elementos sean necesarios para el
funcionamiento inicial.

---

## DEC-006 — Trazabilidad

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

Los resultados producidos por el motor deberán poder
explicar cómo fueron obtenidos.

### Motivo

Un sistema inteligente no debe limitarse a entregar
un número.

Debe ser posible conocer:

- datos utilizados;
- filtros aplicados;
- operaciones realizadas;
- reglas utilizadas;
- resultado obtenido.

### Consecuencia

La trazabilidad será considerada una característica
fundamental del motor.

---

## DEC-007 — Separación del motor respecto al dashboard

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

El dashboard será una interfaz de visualización y
administración, no el lugar donde reside la inteligencia
del sistema.

### Motivo

Evitar que la lógica de negocio quede atrapada dentro
de la interfaz.

### Consecuencia

El dashboard consumirá resultados producidos por
los componentes del sistema.

---

## DEC-008 — Documentar decisiones importantes

**Fecha:** 2026-08-13  
**Estado:** Aprobada

### Decisión

Las decisiones arquitectónicas relevantes deberán
registrarse en este archivo.

### Motivo

Conservar el razonamiento detrás de la evolución
del proyecto.

### Regla

No registrar cada pequeño cambio de código.

Registrar únicamente decisiones que afecten:

- arquitectura;
- filosofía;
- modelo de dominio;
- motor;
- tecnología;
- interoperabilidad;
- seguridad;
- escalabilidad;
- dirección futura del proyecto.

---

## DEC-009 — Finca como tenant soberano y UsuarioFinca como límite de autorización

**Fecha:** 2026-08-19  
**Estado:** Aprobada

### Decisión

En Hato V1, la `Finca` se mantiene como la unidad productiva y tenant
soberano del sistema. La autorización de un usuario sobre una finca se
representa explícitamente mediante `UsuarioFinca`.

La identidad, la autorización y el ámbito de datos quedan separados:

`User` → identidad
`UsuarioFinca` → autorización y rol
`Finca` → ámbito de datos

### Motivo

Se necesitaba aislamiento real entre fincas sin introducir una entidad
`Empresa` artificial y sin depender de parámetros de URL para decidir
qué datos puede consultar un usuario.

### Alternativas consideradas

- introducir una entidad empresarial superior a `Finca`;
- confiar en `?finca=` para determinar el tenant;
- mantener permisos implícitos en las vistas;
- modelar explícitamente la membresía usuario-finca.

Se adopta la última alternativa.

### Consecuencia

La finca activa se resuelve mediante sesión (`finca_activa_id`) y todo
cambio de finca debe pasar por `cambiar_finca_activa`, que verifica una
membresía activa antes de modificar el contexto.

Los usuarios pueden tener diferentes roles en diferentes fincas. Una
membresía puede revocarse mediante `activa=False` sin eliminar historial.

Root/superusuario conserva alcance global y puede fijar un contexto de
finca para operar o auditar dentro de un ámbito concreto.

### Evidencia

La suite `apps/core/test_security_tenant.py` reportó 10/10 pruebas
pasadas, incluyendo aislamiento A→B, manipulación de GET, rechazo POST,
revocación, usuarios multi-finca, cambio de rol y alcance de Root.

---

## DEC-010 — Selección de finca únicamente mediante contexto de sesión validado

**Fecha:** 2026-08-19  
**Estado:** Aprobada

### Decisión

La selección operativa de finca se realiza mediante POST a
`/finca/seleccionar/`, con validación de autorización en servidor.
El sistema no utiliza `?finca=` como mecanismo de autorización o selección
segura del tenant.

### Motivo

Evitar bypass de seguridad mediante manipulación de parámetros de URL y
centralizar la resolución del tenant en el backend.

### Consecuencia

Las vistas sensibles deben obtener la finca desde el contexto de tenant
y comprobar autorización antes de entregar datos. La prueba de seguridad
correspondiente forma parte del contrato verificable de Hato V1.

---

## DEC-011 — Migración no destructiva de membresías existentes

**Fecha:** 2026-08-19  
**Estado:** Aprobada

### Decisión

Las fincas existentes con `created_by` se migran automáticamente a una
membresía `UsuarioFinca` con rol `propietario` y `activa=True` mediante
`0007_migrar_membresias_iniciales.py`.

### Motivo

Incorporar el modelo Multi-Finca sin perder la autoría ni exigir una
reconstrucción manual de los datos existentes.

### Consecuencia

La migración no crea usuarios ficticios ni elimina datos. Las fincas sin
`created_by` quedan disponibles para asignación posterior por Root.

---

## DEC-012 — Catálogos ganaderos globales en Hato V1

**Fecha:** 2026-08-19  
**Estado:** Aprobada

### Decisión

`Especie`, `Raza` y `TipoPasto` permanecen como catálogos globales y no
reciben `finca_id` en esta etapa.

### Motivo

No todo dato del sistema representa datos operativos pertenecientes a
un tenant. Estos catálogos pueden ser compartidos entre fincas sin romper
el aislamiento de los datos operativos.

### Consecuencia

El aislamiento Multi-Finca se aplica al ámbito operativo de cada finca,
mientras los catálogos definidos como universales permanecen compartidos.

---

# FORMATO PARA NUEVAS DECISIONES

Cada nueva decisión deberá seguir esta estructura:

## DEC-XXX — Título

**Fecha:** YYYY-MM-DD  
**Estado:** Propuesta / Aprobada / Reemplazada

### Decisión

¿Qué decidimos?

### Motivo

¿Por qué lo decidimos?

### Alternativas consideradas

¿Qué otras opciones evaluamos?

### Consecuencia

¿Qué cambia como resultado de esta decisión?

con dios y la virgen siempre 

### Notas

Información adicional relevante.

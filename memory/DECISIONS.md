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

La separación permitirá evolucionar cada componente sin
afectar innecesariamente a los demás.

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

### Notas

Información adicional relevante.

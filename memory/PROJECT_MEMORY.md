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

## 6. ARQUITECTURA ACTUAL

Aplicaciones principales:

apps/
├── core
├── ganado
├── mapas
└── administrador

Componentes principales:

core:
    entidades generales de la finca.

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
- primeras implementaciones del motor de métricas.

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

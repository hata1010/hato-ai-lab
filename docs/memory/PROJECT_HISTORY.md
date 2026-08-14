# Hato AI Architect — Historia del proyecto

## Origen y propósito
Hato AI Architect se concibe como un laboratorio de desarrollo humano–IA orientado a construir un sistema capaz de colaborar en el desarrollo, documentar decisiones y conservar continuidad entre sesiones.

## Evolución documentada
- Se estableció `hata1010/hato-ai-lab` como repositorio del proyecto.
- Se creó y validó una GitHub App para que Hato AI Architect pueda operar sobre el repositorio mediante la API de GitHub.
- Se validó la obtención y uso del Installation Token.
- Se realizó una prueba real de escritura y creación de commit mediante la aplicación.
- Se decidió que GitHub será también un lugar persistente para la memoria estructurada del proyecto.
- Se creó `docs/memory/PROJECT_MEMORY.md` como semilla de la memoria persistente.
- Se definió la necesidad de una consolidación histórica de los hilos de trabajo.
- Se definió el concepto `MEMORY_CHECKPOINT` para preservar el estado relevante de un hilo antes de que el contexto se vuelva crítico.

## Principio de continuidad
La continuidad de Hato no debe depender exclusivamente de la permanencia de un hilo de conversación. El conocimiento relevante debe poder convertirse en memoria estructurada y persistirse en el repositorio.

## Criterio de consolidación
Los hilos pueden contener temas ajenos al proyecto. Por tanto, no se deben copiar conversaciones completas. El consolidador debe identificar, filtrar y clasificar únicamente el conocimiento útil para Hato.

## Hitos fundamentales de evolución

### 1. Origen de Hato
Hato surge inicialmente como un sistema orientado a la gestión de una explotación ganadera, utilizando un dominio real para explorar modelado de información, relaciones entre entidades, indicadores y procesos de gestión.

El dominio ganadero se convierte en el primer laboratorio práctico sobre el cual experimentar.

### 2. Evolución hacia un sistema de conocimiento
Durante el desarrollo se identifica que el problema no consiste únicamente en almacenar datos. El sistema necesita representar entidades, relaciones, reglas, eventos, métricas, indicadores, procesos y composición de información.

Esto conduce progresivamente hacia una arquitectura más modular y orientada al conocimiento del dominio.

### 3. Nacimiento del motor de métricas
Uno de los experimentos principales es la construcción de un motor de métricas, capaz de recibir información del dominio y producir resultados mediante una composición estructurada de operaciones.

El motor comienza a separarse conceptualmente de la aplicación ganadera concreta, abriendo la posibilidad de utilizarlo como componente reutilizable.

### 4. Aparición del concepto DSL
Durante la evolución del motor surge la identificación de que las métricas pueden expresarse mediante una forma de lenguaje orientada específicamente al dominio.

Esto lleva al concepto de un lenguaje específico de dominio (DSL) para representar métricas y reglas de cálculo.

Este descubrimiento representa un cambio importante: el proyecto deja de ser solamente una aplicación y comienza a explorar herramientas para describir conocimiento de un dominio.

### 5. Arquitectura modular
El sistema evoluciona hacia una separación de responsabilidades y módulos. La intención pasa a ser construir componentes que puedan evolucionar independientemente, evitando que toda la inteligencia del sistema quede acoplada a una única aplicación.

Esta experiencia se convierte en uno de los fundamentos posteriores de Hato AI Lab.

### 6. Nacimiento de Hato AI Lab
El proyecto se amplía desde el desarrollo de una aplicación concreta hacia un laboratorio de desarrollo humano–IA.

Se crea `hato-ai-lab` como repositorio central. Desde este momento GitHub adquiere una función adicional: no solamente almacenar código, sino conservar el conocimiento y la evolución del proyecto.

El `README.md` establece explícitamente que el repositorio debe funcionar como memoria técnica, conceptual e histórica.

### 7. Nacimiento de Hato AI Architect
A partir de la experiencia acumulada aparece una nueva necesidad: la IA no debería limitarse a responder preguntas o generar fragmentos de código. Debe poder colaborar en la construcción del sistema, comprender su arquitectura, trabajar sobre artefactos y mantener continuidad.

Surge así el concepto de Hato AI Architect.

### 8. GitHub como entorno operativo
Se crea la GitHub App Hato AI Architect y se configura su capacidad de interactuar con el repositorio.

Se obtiene y valida un Installation Token y posteriormente se realiza una escritura real mediante la API.

El archivo `HATO_AI_ARCHITECT_TEST.md` queda como evidencia de esa primera prueba operacional.

Este momento representa el paso de una IA que propone a una IA que puede ejecutar una operación controlada sobre el proyecto.

### 9. GitHub como memoria persistente
A partir de la prueba de integración se establece una decisión fundamental: GitHub será también una capa persistente de memoria del proyecto.

La memoria deja de depender exclusivamente del hilo de conversación. La documentación, decisiones, arquitectura, historia y checkpoints pueden persistirse y versionarse junto al proyecto.

### 10. Nacimiento de la arquitectura de memoria
Se comienza a separar el conocimiento en diferentes niveles.

#### Memoria Fundacional
Conocimiento consolidado, estable y de mayor autoridad.

```text
memory/
├── PROJECT_MEMORY.md
└── DECISIONS.md
```

#### Memoria Evolutiva
Conocimiento producido durante el desarrollo colaborativo:

```text
docs/memory/
├── PROJECT_HISTORY.md
├── CURRENT_STATE.md
├── IMPLEMENTATION_STATUS.md
└── checkpoints/
```

La memoria evolutiva registra el proceso mediante el cual Hato aprende y cambia.

### 11. Nacimiento del Consolidador
Se identifica la necesidad de un mecanismo capaz de analizar el conocimiento producido durante las sesiones y determinar qué debe conservarse.

El principio establecido es:

> No toda conversación es memoria.

El consolidador deberá identificar, filtrar, clasificar y estructurar únicamente aquello que tenga valor para el proyecto.

### 12. Nacimiento de `MEMORY_CHECKPOINT`
Se define `MEMORY_CHECKPOINT` como mecanismo para preservar un estado significativo del conocimiento antes de perder continuidad.

El primer checkpoint registrado es:

```text
MC-2026-08-14-001
```

Esto convierte el concepto de checkpoint en una estructura real dentro del repositorio.

### 13. Descubrimiento del protocolo de sincronización
Durante la evolución del proyecto se identifica una diferencia fundamental:

```text
CONTEXTO DE CONVERSACIÓN
        ≠
ESTADO REAL DEL PROYECTO
```

La conversación permite recuperar intención y contexto, pero el repositorio debe utilizarse para verificar el estado técnico real.

De este descubrimiento surge el protocolo:

> “Vamos a sincronizar Hato.”

La sincronización combina contexto disponible, memoria persistente y estado actual del repositorio antes de continuar una construcción cuando existe riesgo de desfase.

## Arquitectura conceptual de la memoria

La evolución del proyecto establece una separación entre memoria fundacional y memoria evolutiva.

```text
              HATO AI
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
 MEMORIA FUNDACIONAL   MEMORIA EVOLUTIVA
        │                 │
   estable/autoridad   colaborativa/dinámica
        │                 │
        │            experimentos
        │            descubrimientos
        │            aprendizajes
        │                 │
        │                 ▼
        │            CONSOLIDADOR
        │                 │
        └───────────◄─────┘
              validación
```

La memoria evolutiva registra cómo Hato aprende; la memoria fundacional conserva aquello que Hato ha consolidado como conocimiento.

La transición entre ambas requiere filtrado, clasificación y validación. El conocimiento evolutivo no se convierte automáticamente en conocimiento fundacional.

# Manual de Colaboración Humano–IA sobre Arquitectura de Contexto Externo

**Proyecto:** Hato AI Lab  
**Versión:** 1.0  
**Fecha:** 2026-08-18  
**Estado:** Experimental / operativo

## 1. Propósito

Este manual define el procedimiento para incorporar una inteligencia artificial a un proyecto que utiliza **memoria externa persistente, código fuente y colaboración entre varias IAs**.

El objetivo es que una IA pueda trabajar sobre el proyecto sin depender de una conversación anterior y sin inventar elementos de la arquitectura cuando no dispone de información suficiente.

El principio central es:

> **La IA trabaja sobre el contexto del proyecto; la memoria del proyecto pertenece al repositorio.**

## 2. Principios fundamentales

1. **El repositorio es la fuente de verdad.**
2. **La memoria externa conserva el contexto que no debe depender del chat.**
3. **La IA debe distinguir hechos, inferencias y propuestas.**
4. **No se deben inventar modelos, campos, aplicaciones, archivos o componentes para completar una solución.**
5. **Si falta información, la IA debe declararlo explícitamente.**
6. **La implementación debe respetar la arquitectura existente antes de proponer una arquitectura nueva.**
7. **La persona responsable del proyecto mantiene la dirección y la decisión final.**
8. **Varias IAs pueden participar con funciones diferentes; no es necesario que todas tengan las mismas capacidades.**

## 3. Las tres capas de contexto

Una IA puede recibir información mediante tres capas:

### 3.1 Memoria del proyecto

Incluye, según corresponda:

- propósito del proyecto;
- decisiones;
- arquitectura;
- estado actual;
- historial;
- experimentos;
- contratos y protocolos;
- resultados y aprendizajes.

La memoria permite reconstruir el contexto conceptual e histórico.

### 3.2 Código fuente

El código es la fuente de verdad para comprobar:

- modelos;
- campos;
- relaciones;
- funciones;
- interfaces;
- configuraciones;
- pruebas;
- componentes realmente implementados.

La IA no debe sustituir esta verificación por suposiciones.

### 3.3 Instrucción humana

La persona define:

- el objetivo;
- las restricciones;
- el alcance;
- los datos de prueba;
- el nivel de autonomía permitido;
- la decisión final.

## 4. Protocolo de incorporación de una IA

Toda IA nueva debe seguir esta secuencia.

### Paso 1 — Recibir la tarea

Identificar exactamente qué se solicita y qué queda fuera del alcance.

### Paso 2 — Leer la memoria externa

Consultar primero la documentación relevante del proyecto antes de formular una solución.

### Paso 3 — Determinar la capacidad de acceso

La IA debe declarar si puede:

- leer directamente el repositorio;
- leer archivos suministrados;
- leer únicamente documentación;
- o trabajar solo con información proporcionada en la conversación.

### Paso 4 — Inspeccionar el código disponible

Cuando tenga acceso al código, debe buscar y verificar los componentes relacionados con la tarea.

Debe identificar rutas, clases, funciones, campos y relaciones reales.

### Paso 5 — Separar hechos de suposiciones

La respuesta debe distinguir claramente:

- **Hecho:** comprobado en memoria o código.
- **Inferencia:** deducción razonable basada en información disponible.
- **Propuesta:** solución que todavía no forma parte del proyecto.
- **Desconocido:** información que no pudo verificarse.

### Paso 6 — Comprobar suficiencia de datos

Antes de programar, responder:

> ¿La estructura actual contiene todos los datos necesarios?

Si la respuesta es no, se debe describir exactamente qué falta.

### Paso 7 — Proponer la solución

La propuesta debe reutilizar primero los componentes existentes.

Una arquitectura nueva solo debe proponerse cuando exista una necesidad demostrada.

### Paso 8 — Validación humana

Cuando el cambio sea arquitectónico o pueda afectar código existente, la IA debe esperar la decisión humana antes de modificar el proyecto, salvo que se haya autorizado explícitamente la implementación.

### Paso 9 — Implementar

Implementar únicamente el alcance aprobado.

### Paso 10 — Probar

Crear o ejecutar pruebas que demuestren el comportamiento esperado y los casos límite relevantes.

### Paso 11 — Documentar

Registrar decisiones, resultados, limitaciones y aprendizajes relevantes.

### Paso 12 — Actualizar memoria

Si el trabajo cambia el conocimiento permanente del proyecto, actualizar la memoria correspondiente.

## 5. Protocolo para IAs que no pueden leer directamente el repositorio

Una IA sin acceso directo al código **no queda descartada**.

Debe recibir un paquete de contexto preparado por una IA o persona con acceso al repositorio.

### Paquete mínimo de contexto

1. Fragmento o archivo de memoria relevante.
2. Estado actual relevante.
3. Archivos fuente necesarios para la tarea.
4. Restricciones conocidas.
5. Objetivo de la tarea.
6. Datos de prueba.
7. Preguntas concretas que debe analizar.

La IA receptora debe tratar esos archivos como su contexto técnico disponible y señalar explícitamente cualquier parte que no pueda verificar.

## 6. Modelo de colaboración entre varias IAs

Las IAs pueden asumir roles diferentes.

### IA exploradora

Responsable de inspeccionar el repositorio y localizar:

- componentes existentes;
- relaciones;
- datos disponibles;
- limitaciones.

### IA implementadora

Responsable de convertir una solución aprobada en código y pruebas.

### IA analista o segunda opinión

Responsable de revisar una propuesta utilizando memoria y archivos suministrados, aunque no tenga acceso directo al repositorio.

### IA crítica

Responsable de buscar:

- supuestos no demostrados;
- inconsistencias;
- errores de diseño;
- riesgos;
- casos no contemplados.

### Humano responsable

Mantiene:

- dirección del proyecto;
- aceptación o rechazo de propuestas;
- control del alcance;
- decisión arquitectónica final.

## 7. Flujo colaborativo recomendado

```text
                 TAREA HUMANA
                       |
                       v
                MEMORIA EXTERNA
                       |
                       v
              IA CON ACCESO AL CÓDIGO
                       |
            inspección y contexto real
                       |
          +------------+------------+
          |                         |
          v                         v
    IA implementadora        IA segunda opinión
          |                         |
          +------------+------------+
                       |
                       v
                  IA crítica
                       |
                       v
                DECISIÓN HUMANA
                       |
                       v
                 IMPLEMENTACIÓN
                       |
                       v
                    PRUEBAS
                       |
                       v
                  DOCUMENTACIÓN
                       |
                       v
                 MEMORIA NUEVA
```

## 8. Regla de oro: no rellenar vacíos inventando

Cuando una IA no encuentra un elemento necesario debe responder, por ejemplo:

> **NO ENCONTRADO:** no existe evidencia en los archivos suministrados de un modelo que registre el tipo de servicio reproductivo.

Y después:

1. indicar qué sí existe;
2. indicar qué falta;
3. explicar qué impide calcular o implementar;
4. proponer el mínimo cambio posible, si corresponde;
5. esperar aprobación antes de modificar la arquitectura.

Una respuesta que reconoce correctamente una limitación es preferible a una implementación completa basada en datos inventados.

## 9. Protocolo para métricas, reportes e indicadores

Antes de construir una métrica, la IA debe seguir este orden:

```text
Objetivo
  ↓
Datos necesarios
  ↓
Datos existentes
  ↓
Relaciones reales
  ↓
Datos faltantes
  ↓
Fórmula
  ↓
Resultado de prueba
  ↓
Implementación
  ↓
Validación
```

Para cada métrica debe quedar registrado, cuando aplique:

- nombre;
- código o identificador;
- propósito;
- entradas;
- origen de cada entrada;
- fórmula;
- unidad;
- período;
- contexto;
- casos límite;
- resultado esperado;
- pruebas;
- limitaciones.

## 10. Experimento de referencia: GMD

La Ganancia Media Diaria permitió validar el protocolo.

Datos de prueba:

- peso inicial: 200 kg;
- fecha inicial: 2026-06-01;
- peso final: 225 kg;
- fecha final: 2026-07-01.

Fórmula:

```text
GMD = (peso_final - peso_inicial) / días
```

Resultado:

```text
(225 - 200) / 30 = 0.833 kg/día
```

El experimento demostró que una IA con capacidad de inspeccionar el código puede descubrir la estructura real y reutilizar componentes existentes, mientras que otra IA puede aportar una segunda opinión si recibe memoria y archivos suficientes.

## 11. Evaluación de una IA colaboradora

No evaluar una IA únicamente por la cantidad o velocidad del código generado.

Evaluar al menos:

| Capacidad | Pregunta |
|---|---|
| Acceso | ¿Puede leer el código real? |
| Contexto | ¿Utiliza la memoria externa? |
| Comprensión | ¿Encuentra los componentes correctos? |
| Verificación | ¿Distingue hechos de supuestos? |
| Arquitectura | ¿Respeta lo existente? |
| Datos | ¿Detecta información faltante? |
| Implementación | ¿Produce código correcto? |
| Pruebas | ¿Valida casos normales y límite? |
| Crítica | ¿Detecta errores en propuestas? |
| Continuidad | ¿Deja conocimiento reutilizable? |

## 12. Regla de comparación entre IAs

Cuando se comparen dos IAs, deben recibir:

- la misma tarea;
- las mismas restricciones;
- los mismos datos de prueba;
- el mismo objetivo;
- y, cuando sea posible, el mismo paquete de contexto.

La comparación debe separar:

1. capacidad de descubrir contexto;
2. capacidad de razonar sobre el contexto;
3. capacidad de implementar;
4. capacidad de revisar el trabajo de otra IA.

Una IA que no puede acceder directamente al repositorio puede seguir siendo valiosa como analista o segunda opinión si trabaja con un contexto externo correctamente preparado.

## 13. Control humano

La colaboración humano–IA no elimina la responsabilidad humana.

La IA puede:

- explorar;
- analizar;
- programar;
- probar;
- criticar;
- documentar;
- proponer.

La persona responsable decide:

- qué construir;
- qué aceptar;
- qué rechazar;
- qué modificar;
- cuándo publicar;
- cuándo cambiar la arquitectura.

## 14. Persistencia del conocimiento

Un resultado importante no debe permanecer solamente en el chat.

Cuando un experimento produzca una conclusión reutilizable, debe convertirse en documentación o memoria del proyecto.

De esta manera:

```text
Conversación
    ↓
Experimento
    ↓
Resultado
    ↓
Conclusión
    ↓
Memoria/documentación
    ↓
Nuevo contexto para futuras IAs
```

## 15. Criterio de madurez

La arquitectura colaborativa se considera madura cuando una IA nueva puede:

1. leer la memoria;
2. entender el propósito del proyecto;
3. identificar su capacidad de acceso;
4. estudiar el código disponible;
5. localizar componentes existentes;
6. evitar inventar arquitectura;
7. producir una propuesta verificable;
8. recibir crítica de otra IA;
9. implementar cambios aprobados;
10. dejar documentación suficiente para que otra IA pueda continuar.

## 16. Principio final

> **No buscamos una IA que lo haga todo. Buscamos una arquitectura en la que distintas IAs puedan aportar sus capacidades, compartir contexto y ser verificadas por otras IAs y por la persona responsable del proyecto.**

La memoria externa convierte al proyecto en el punto común de continuidad.

El código representa el estado real.

Las IAs aportan capacidades diferentes.

La colaboración produce conocimiento.

Y el conocimiento validado vuelve al repositorio para que pueda ser utilizado por la siguiente IA.

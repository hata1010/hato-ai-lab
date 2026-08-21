# Diseño de modelos — Reproducción y Lactancia

## 1. Objetivo

Definir el modelo de captura histórica necesario para que Hato pueda registrar reproducción y producción de leche sin alterar todavía los modelos Django ni crear migraciones.

Cadena de diseño:

`Animal → eventos reproductivos → parto/cría → lactación → controles de leche → Motor de Métricas`

## 2. Principios

- Reutilizar `Animal`, `Finca` y la genealogía existente.
- Mantener trazabilidad por animal y finca.
- Un evento histórico no se sobrescribe para corregir el pasado: se registra el dato correcto y se conserva auditoría.
- No inventar fechas, resultados ni mediciones.
- Unidades explícitas para magnitudes productivas.
- Fechas efectivas separadas de fechas de registro cuando sea necesario.
- La fuente del dato debe poder identificarse.
- Las métricas se derivan; no se almacenan como hechos si pueden calcularse desde el historial.

## 3. Modelo propuesto: EventoReproductivo

Representa un hecho reproductivo asociado principalmente a una hembra.

### Campos

- `animal`: FK a `Animal`; obligatorio; debe ser hembra para eventos de ciclo reproductivo de hembra.
- `finca`: FK a `Finca`; obligatorio; debe coincidir con la finca del animal al momento del evento.
- `tipo`: catálogo versionable: celo, servicio, diagnóstico_gestacion, aborto, perdida_gestacional, parto, destete, otro.
- `fecha`: fecha efectiva del evento.
- `fecha_registro`: fecha/hora de captura.
- `resultado`: catálogo según tipo; por ejemplo positivo/negativo/no_concluyente para diagnóstico.
- `padre_cria`: FK opcional a `Animal` para identificar el semental cuando sea conocido.
- `metodo_servicio`: natural, IA, transferencia_embrión, desconocido; aplica cuando corresponda.
- `numero_servicio`: entero positivo opcional dentro de una secuencia reproductiva.
- `observaciones`: texto.
- `fuente_dato`: catálogo/origen del registro.
- `usuario_registro`: usuario responsable cuando la arquitectura de permisos lo permita.

### Validaciones

- El animal debe existir y pertenecer a la finca.
- Los eventos incompatibles con sexo deben rechazarse.
- Un servicio requiere fecha y método.
- Un diagnóstico debe estar asociado a una gestación/servicio cuando la trazabilidad disponible lo permita.
- Un parto no puede preceder al servicio/gestación relacionado si estos datos fueron registrados.
- El semental debe ser macho y de la misma especie; la finca puede ser distinta si el modelo futuro permite servicio externo, pero debe quedar explícito.
- No duplicar el mismo evento mediante una clave de negocio definida con tipo + animal + fecha + secuencia cuando aplique.

## 4. Modelo propuesto: CriaNacimiento

Aunque `Animal` ya tiene padre/madre y fecha de nacimiento, se requiere un evento histórico para conservar el hecho del nacimiento.

### Campos

- `parto`: FK a `EventoReproductivo` de tipo parto.
- `cria`: FK a `Animal`, cuando la cría ya fue registrada.
- `fecha_nacimiento`: fecha/hora efectiva si difiere de la fecha del parto.
- `sexo`: opcional mientras la cría no esté formalizada como Animal.
- `peso_nacimiento`: decimal opcional con unidad kg.
- `tipo_parto`: normal, asistido, distócico, cesárea, otro.
- `estado_cria`: viva, muerta, no_determinada.
- `observaciones`.
- `fuente_dato`.

La relación `Animal.padre`/`Animal.madre` sigue siendo la referencia genealógica actual; el evento conserva la historia temporal.

## 5. Modelo propuesto: Lactacion

Representa una lactación de una hembra.

### Campos

- `animal`: FK a `Animal`.
- `finca`: FK a `Finca`.
- `numero_lactacion`: entero positivo.
- `fecha_inicio`: fecha efectiva, normalmente vinculada al parto cuando se conoce.
- `fecha_fin`: opcional hasta secado/fin de lactación.
- `parto`: FK opcional a `EventoReproductivo`.
- `estado`: abierta, cerrada, interrumpida.
- `observaciones`.
- `fuente_dato`.

### Validaciones

- Animal debe ser hembra y pertenecer a la finca.
- `fecha_fin >= fecha_inicio`.
- No debe haber dos lactaciones abiertas simultáneas para el mismo animal.
- El número de lactación debe ser positivo.
- Si existe parto asociado, la finca y animal deben coincidir.

## 6. Modelo propuesto: ControlLeche

Representa una medición individual de producción, no una métrica agregada.

### Campos

- `lactacion`: FK a `Lactacion`.
- `fecha_hora`: momento de la medición.
- `cantidad`: decimal positiva.
- `unidad`: catálogo; kg o L, sin mezclar unidades dentro de una serie sin conversión explícita.
- `turno`: mañana, tarde, noche, único, otro.
- `metodo_medicion`: báscula, medidor, estimación, otro.
- `grasa`: decimal opcional.
- `proteina`: decimal opcional.
- `celulas_somaticas`: decimal opcional con unidad documentada.
- `observaciones`.
- `fuente_dato`.
- `usuario_registro`.

### Validaciones

- Cantidad no negativa.
- La lactación debe estar abierta o permitir registros históricos explícitos.
- Fecha de medición dentro del periodo de lactación cuando las fechas estén disponibles.
- Unidad obligatoria.
- Los componentes de calidad deben validar rangos razonables definidos por catálogo/metodología, no valores arbitrarios en código.

## 7. Captura en interfaz

### Reproducción

La captura debe comenzar seleccionando finca y animal. El formulario cambia según el tipo de evento y muestra solamente los campos pertinentes.

Flujo mínimo:

`Finca → Animal → Tipo de evento → Fecha efectiva → Datos específicos → Fuente → Observación → Guardar`

### Lactancia

`Finca → Hembra → Lactación → Fecha → Producción → Unidad → Turno → Método → Calidad opcional → Fuente → Guardar`

El sistema debe mostrar el contexto del animal y evitar que el operador tenga que repetir información derivable.

## 8. Auditoría

Todo registro debe poder responder:

- ¿a qué animal pertenece?
- ¿a qué finca pertenece?
- ¿cuándo ocurrió?
- ¿cuándo se registró?
- ¿quién lo registró?
- ¿cuál fue la fuente?
- ¿qué unidad se utilizó?
- ¿qué observación/evidencia existe?

## 9. Métricas habilitadas

### Reproducción

- tasa de concepción;
- tasa de preñez;
- servicios por concepción;
- días abiertos;
- intervalo entre partos;
- edad al primer servicio;
- edad al primer parto;
- duración de gestación.

### Lactancia

- producción por control;
- producción acumulada;
- producción por lactación;
- duración de lactación;
- producción estandarizada cuando exista metodología aprobada;
- producción por día;
- composición/calidad cuando haya datos suficientes.

Las fórmulas no se fijan en estos modelos. Se definirán en el Motor de Métricas con versión, unidad, fuente y alcance.

## 10. Compatibilidad con modelos existentes

`Animal` ya contiene finca, sexo, fecha de nacimiento y genealogía, por lo que no se debe duplicar esa información. `PesajeAnimal`, `EventoSalud` y `MovimientoAnimal` continúan siendo fuentes independientes para peso, salud y localización.

## 11. Orden de implementación

1. Crear modelos y catálogos mínimos.
2. Migraciones.
3. Admin/formularios.
4. Validaciones y pruebas.
5. Captura histórica inicial.
6. Conectar variables al Motor de Métricas.
7. Indicadores.
8. Panel.

## 12. Estado

**DISEÑO CONCLUIDO — NO IMPLEMENTADO.**

Este documento es una especificación previa a código. No autoriza por sí mismo la creación de migraciones.

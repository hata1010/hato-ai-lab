# Fase 4 — PDF y documentos

## Propósito

Construir una capacidad documental independiente del Motor de Métricas, capaz de recibir documentos y representarlos de forma estructurada.

La fase no incorpora todavía interpretación semántica avanzada, OCR, visión artificial ni integración con el Motor de Métricas.

## Modelo conceptual

```text
Documento
├── texto
├── tablas
├── imágenes
├── metadatos
└── estructura
```

## Subfases

### 4.1 — Inventario de formatos

**Objetivo:** definir los formatos iniciales soportados y sus capacidades.

Tareas:

- Identificar formatos iniciales: PDF, DOCX y eventualmente imágenes independientes.
- Determinar qué elementos puede contener cada formato.
- Definir qué se considera documento válido.
- Definir límites iniciales de tamaño.
- Registrar las decisiones en la documentación del proyecto.

Especificación inicial:

| Formato | Contenido esperado |
|---|---|
| PDF | texto + tablas + imágenes + metadatos |
| DOCX | texto + tablas + imágenes + estructura |
| IMG | imagen + metadatos |

**Criterio de cierre:** la especificación queda documentada y sirve como contrato para la subfase 4.2.

### 4.2 — Modelo documental

Definir la representación interna común del documento: identificación, metadatos, estructura, páginas/secciones, texto, tablas e imágenes.

**Resultado:** contrato/modelo documental.

### 4.3 — Extractor documental

Construir un componente independiente que reciba un documento y produzca una representación estructurada.

Para PDF se evaluará extracción de texto, páginas, metadatos, imágenes, tablas cuando sean detectables y estructura básica.

Para DOCX se evaluará extracción de párrafos, títulos, tablas, imágenes, orden y metadatos disponibles.

**Implementación V1:** `tools/document_extractor.py` contiene el contrato `DocumentModel`, los elementos ordenados `DocumentElement`, identificación mediante tamaño/hash y extractores para PDF, DOCX e imágenes. PDF usa `pypdf` y tablas mediante `pdfplumber` cuando está disponible; DOCX usa `python-docx`; imágenes usan Pillow para dimensiones/EXIF cuando está disponible. Las dependencias específicas se cargan de forma opcional y los errores de extracción se representan mediante excepciones controladas.

**Pruebas iniciales:** `tools/test_document_extractor.py` verifica detección por firma, identificación/hash de imagen y manejo controlado de formatos no soportados.

**Resultado:** extractor documental independiente implementado. Las pruebas de contenido real PDF/DOCX quedan para 4.4 y 4.5, respectivamente.

### 4.4 — Prueba PDF universal

Crear un PDF controlado con título, texto, tabla e imagen y verificar qué componentes puede extraer el sistema.

**Ejecución realizada:** se creó un PDF controlado de una página con título, texto, tabla de datos e imagen. La prueba se ejecutó con `pypdf 5.9.0` y `pdfplumber 0.11.9`.

**Resultados observados:**

| Componente | Resultado |
|---|---|
| Identificación del PDF | ✅ Detectado por firma PDF |
| Número de páginas | ✅ 1 |
| Metadatos | ✅ Título y autor recuperados |
| Texto | ✅ Extraído correctamente |
| Tabla | ✅ Detectada y extraída: 4 filas × 2 columnas |
| Imagen | ✅ 1 imagen detectada y recuperada |
| Estructura básica | ✅ Página y elementos extraídos en orden |

**Conclusión 4.4:** la prueba PDF universal fue satisfactoria. El extractor V1 demuestra que puede convertir un PDF controlado con texto, tabla, imagen y metadatos en una representación estructurada. No se detectó una limitación que requiera modificar el contrato documental en esta subfase.

### 4.5 — Prueba DOCX

Crear un DOCX controlado con título, texto, tabla, imagen y texto adicional y verificar la extracción.

### 4.6 — Comparación PDF vs DOCX

Registrar objetivamente la capacidad obtenida para texto, tablas, imágenes, metadatos, estructura y orden.

### 4.7 — Documentos problemáticos

Probar documentos solamente con texto, escaneados, con texto e imagen, con tablas, vacíos, inválidos o corruptos, verificando fallos controlados.

### 4.8 — Resultado normalizado

Definir un formato común para que PDF, DOCX e imágenes puedan representarse mediante un documento normalizado y una colección ordenada de elementos.

### 4.9 — Trazabilidad

Cada elemento extraído debe poder relacionarse con su origen documental, por ejemplo documento → página → elemento.

### 4.10 — Integración mínima con Hato

Integrar el extractor de forma mínima con Hato, inicialmente mediante una interfaz de prueba; no construir todavía una interfaz documental completa.

### 4.11 — Pruebas automatizadas

Crear pruebas para las capacidades soportadas y para errores controlados.

Ejemplos:

- PDF con texto.
- PDF con imagen.
- PDF con tabla.
- DOCX con texto.
- DOCX con imagen.
- DOCX con tabla.
- Documento vacío.
- Documento inválido.

### 4.12 — Documentación

Documentar formatos soportados, modelo documental, extractor y resultados de las pruebas. Cualquier entidad o campo persistente nuevo deberá reflejarse también en el diccionario de datos.

### 4.13 — Cierre de Fase 4

La fase se considerará cerrada cuando exista evidencia de que los formatos definidos pueden recibirse y convertirse a una representación estructurada normalizada, con trazabilidad y pruebas automatizadas, dentro de los límites documentados.

## Reglas de alcance

- El Motor de Métricas permanece separado.
- No se incorpora OCR en esta fase salvo que una prueba posterior demuestre que es necesario y se documente como decisión.
- No se incorpora interpretación semántica avanzada.
- No se incorpora visión artificial.
- Cada capacidad nueva se prueba inmediatamente.
- El repositorio es la fuente de verdad de esta planificación y de sus resultados.

## Estado

- Fase 4: en ejecución.
- Subfase 4.1: especificación inicial documentada y tareas iniciales ejecutadas.
- Subfase 4.2: contrato/modelo documental definido.
- Subfase 4.3: extractor documental V1 implementado y pruebas iniciales añadidas.
- Subfase 4.4: **cerrada satisfactoriamente** con PDF universal controlado.
- Próximo paso: ejecutar 4.5 con un DOCX controlado.

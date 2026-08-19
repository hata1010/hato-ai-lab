# 📖 DICCIONARIO OFICIAL DE TÉRMINOS — SISTEMA HATO

**Proyecto:** Hato AI Lab  
**Documento:** Glosario conceptual del dominio  
**Versión:** 1.1  
**Fecha:** 2026-08-19  
**Estado:** Oficial para el diseño conceptual; las definiciones pueden evolucionar mediante una decisión documentada.

---

## 1. Propósito

Este documento define el significado de los términos utilizados por Hato en el dominio ganadero y productivo.

No es un diccionario técnico de campos de base de datos. Para los nombres, tipos, llaves y restricciones del modelo Django se utiliza `docs/DATA_DICTIONARY.md`.

El objetivo es que personas, código e inteligencias artificiales compartan un lenguaje de dominio común. La primera capa del diccionario se orienta deliberadamente al vocabulario más común de **Colombia y Venezuela**, incluyendo sinónimos y variantes regionales cuando sean relevantes.

Hato no pretende construir inicialmente un glosario universal. La evolución prevista es: **primero lenguaje regional, después consolidación latinoamericana, luego correspondencias internacionales y finalmente conocimiento de dominio utilizable por la IA**.

> **Una definición conceptual adoptada por Hato no debe cambiarse por interpretación informal. Si necesita modificarse, debe registrarse como decisión del proyecto.**

> **Regla regional:** cuando un término tenga variaciones entre Colombia, Venezuela u otras regiones, Hato conservará el uso regional documentado y evitará presentar una equivalencia local como universal.

---

## 2. Principios conceptuales

### Finca

En Hato, una **finca** es una **unidad productiva ganadera independiente**. Es el centro operativo del sistema: posee o administra sus animales, potreros, corrales, instalaciones, producción, movimientos, documentos y demás recursos asociados.

Una finca no se considera automáticamente una sucursal o componente subordinado de una entidad llamada Empresa. La relación entre finca y empresa legal queda fuera de esta definición mientras no exista una decisión arquitectónica explícita que adopte ese modelo.

### Empresa

**Empresa** es un concepto legal, administrativo o comercial que puede existir alrededor de una explotación ganadera, pero **Hato no adopta en este glosario una jerarquía obligatoria `Empresa → múltiples Fincas`**.

Si posteriormente se requiere multiempresa corporativo, deberá definirse explícitamente la relación jurídica y de propiedad sin alterar retrospectivamente el significado operativo de finca.

### Hato

**Hato** es la explotación ganadera o conjunto organizado de recursos y animales gestionados como una unidad productiva. En el sistema, el término se relaciona conceptualmente con la finca y con la actividad ganadera que esta desarrolla.

### Animal

Individuo perteneciente a una especie registrada en Hato y gestionado individualmente mediante un identificador, historial y atributos productivos, sanitarios o genealógicos.

### Ganado

Conjunto de animales de una explotación ganadera. En Hato puede referirse al inventario de animales de una finca, especialmente cuando se habla de población, manejo o producción.

---

## 3. Categorías ganaderas y etapas de desarrollo

Estas definiciones describen categorías productivas o etapas de desarrollo. No sustituyen automáticamente los datos de fecha de nacimiento, sexo, raza u otros atributos del animal. Los límites de edad pueden variar según región y sistema productivo y, cuando sean necesarios para una métrica, deberán quedar definidos explícitamente.

### Vaca

Hembra bovina adulta. En Hato, el término identifica una categoría productiva asociada principalmente a reproducción y/o producción, según el manejo de la finca.

### Toro

Macho bovino adulto destinado principalmente a reproducción.

### Padrote / Reproductor

Toro adulto seleccionado y utilizado para reproducción, especialmente mediante monta natural. **Padrote** es un término de uso ganadero regional frecuente, mientras que **reproductor** es una denominación más general.

### Novilla

Hembra bovina joven que aún no se considera vaca adulta. La transición de novilla a vaca depende del criterio productivo adoptado por la explotación y de la situación reproductiva.

### Novillo

Macho bovino joven que ha superado la etapa temprana de becerro y que todavía no corresponde a la categoría de toro reproductor. Puede estar destinado a crecimiento, levante, engorde o producción de carne.

### Becerro / Becerra

Bovino joven en la primera etapa de desarrollo. **Becerro** suele referirse al macho y **becerra** a la hembra. La frontera exacta entre becerro/a, destetado/a y categorías posteriores puede variar regionalmente.

### Maute / Mauta

Término ganadero de uso regional, especialmente en Venezuela y zonas de influencia, para referirse a un bovino joven después del destete y antes de las categorías adultas. Su rango exacto de edad no se fija como universal en Hato.

### Torete

Macho bovino joven en desarrollo, generalmente relacionado con un futuro reproductor. No debe confundirse automáticamente con toro adulto.

### Destete / Destetado

**Destete** es el proceso de separación del animal joven de la alimentación directa de la madre. **Destetado** describe al animal que ya pasó por ese proceso. El momento y edad del destete pueden variar según el sistema productivo.

### Vaca parida

Vaca que ha tenido una cría recientemente. El término describe una condición reproductiva y no equivale automáticamente a estar en ordeño.

### Vaca en ordeño

Vaca en período activo de producción de leche y sometida al manejo de ordeño de la finca.

### Vaca horra / vaca seca

Vaca adulta que no se encuentra en producción de leche en ese momento. **Vaca seca** suele referirse al período de descanso de la lactancia previo al siguiente parto; **horra** puede utilizarse regionalmente con un alcance más amplio según el manejo.

### Vaca escotera

Término regional cuyo significado puede variar. En el contexto ganadero de Hato se conservará como término de campo asociado a una vaca que, según el uso local, no está acompañada de cría o no está cumpliendo determinada condición reproductiva. Cuando se use para una regla de negocio deberá especificarse el significado exacto adoptado por la finca.

### Descarte / Refugo

Animal separado del grupo productivo para venta, reemplazo o sacrificio por razones como edad, desempeño, problemas reproductivos, sanitarios o productivos. **Refugo** es una variante regional.

### Caballo

Animal de la especie equina. Se conserva en el glosario porque puede formar parte de una explotación ganadera y de su inventario de animales, aunque el modelo productivo actual de Hato esté centrado principalmente en ganado bovino.

---

## 4. Biología, raza y genética

### Especie

Categoría biológica a la que pertenece un animal. En el modelo actual puede incluir bovinos, bufalinos, caprinos u otras especies que el sistema llegue a soportar.

### Raza

Grupo o clasificación zootécnica dentro de una especie que reúne características hereditarias y fenotípicas reconocidas.

### Genética

Conjunto de características hereditarias de un animal y la información relacionada con su transmisión biológica.

### Composición genética

Representación de la participación porcentual de una o varias razas en la constitución genética de un animal. Ejemplo conceptual: 50 % Brahman + 50 % Gyr.

La composición genética no debe confundirse con la raza declarada: un animal puede tener una raza declarada y, simultáneamente, una composición genética multirracial documentada.

### Pedigrí / genealogía

Información sobre ascendencia de un animal, incluyendo padre, madre y demás antecesores conocidos o registrados.

---

## 5. Territorio, superficie y georreferenciación

### Potrero

Área delimitada dentro de una finca destinada principalmente al pastoreo y manejo de animales. Puede disponer de geometría, superficie, capacidad y estado operativo.

### Corral

Instalación delimitada destinada al confinamiento, manejo, clasificación, tratamiento, embarque u otras operaciones con animales.

### Hectárea (ha)

Unidad estándar de superficie utilizada por Hato para áreas productivas. **1 ha = 10.000 m²**.

### Metro cuadrado (m²)

Unidad de superficie utilizada para mediciones de terrenos, corrales, instalaciones y muestreos de aforo.

### Metro lineal (m)

Unidad de longitud utilizada, entre otros usos, para linderos, cercas, comederos, bebederos y frentes de pastoreo.

### Cuadra / Plaza / Fanegada

Medidas agrarias tradicionales cuyo valor puede variar regionalmente. En el contexto inicial de Hato se documentarán equivalencias locales sin asumir que una sola conversión sea válida para todo Colombia o Venezuela.

### Kilómetro cuadrado (km²)

Unidad de superficie equivalente a **100 ha**. Puede resultar útil para extensiones territoriales grandes.

### Polígono GPS

Representación geométrica de un área delimitada mediante coordenadas geográficas. En el sistema puede utilizarse para representar el perímetro de un potrero.

### Aforo forrajero

Muestreo de campo destinado a estimar la cantidad de biomasa forrajera disponible en una superficie determinada. Puede expresarse, según el método, como kg de materia verde por m² o kg de materia seca por ha.

---

## 6. Pasturas, pastoreo y carga

### Pastura / pasto

Vegetación forrajera disponible para alimentación de los animales. En Hato puede representarse mediante un tipo de pasto o una clasificación relacionada con el manejo del potrero.

### Pasto de corte

Forraje cultivado para ser cosechado y suministrado posteriormente a los animales, en lugar de ser consumido directamente en el área de cultivo.

### Ensilaje / silo

Forraje conservado mediante fermentación controlada, normalmente en condiciones anaeróbicas, para utilizarlo como reserva alimenticia.

### Heno

Forraje conservado mediante deshidratación, normalmente con humedad suficientemente baja para permitir su almacenamiento.

### Sal mineralizada

Suplemento compuesto por sal y minerales destinado a complementar la dieta del ganado según las necesidades del sistema productivo.

### Melaza

Subproducto líquido de la producción de azúcar, utilizado como suplemento energético y/o palatabilizante en determinados sistemas de alimentación.

### Pastoreo

Actividad mediante la cual los animales utilizan una superficie de pastura para alimentarse durante un período determinado.

### Pastoreo racional / PRV

Sistema de manejo que organiza la ocupación y descanso de las áreas de pastoreo buscando mejorar el aprovechamiento y recuperación de las pasturas. Hato no presupone que toda finca utilice PRV.

### Movimiento animal

Registro de entrada, permanencia y salida de un animal de un potrero u otra ubicación operativa.

### Período de ocupación

Tiempo durante el cual un animal o lote permanece en un potrero determinado.

### Período de descanso

Tiempo transcurrido entre la salida de animales de un potrero y su siguiente ocupación, utilizado para evaluar la recuperación de la pastura.

### Carga animal

Cantidad de animales asociada a una determinada superficie productiva durante un período o momento de análisis. Puede expresarse, según la métrica, como cabezas por hectárea u otra unidad definida.

### Unidad Gran Ganado (UGM)

Unidad de referencia utilizada para comparar cargas animales de individuos de diferente peso. Hato podrá adoptar una equivalencia concreta para sus métricas cuando sea necesario; la equivalencia no se presenta aquí como universal.

---

## 7. Agua e infraestructura hídrica

### Punto de agua / fuente de agua

Lugar o instalación donde existe disponibilidad de agua para consumo animal, uso doméstico, riego u otra necesidad de la finca.

### Bebedero / abrevadero

Instalación destinada a suministrar agua al ganado para consumo.

### Pozo profundo / perforado

Captación de agua subterránea mediante perforación y sistema de extracción.

### Pozo artesiano / aljibe

Términos regionales relacionados con captaciones de agua subterránea. Su significado técnico exacto puede variar según el tipo de obra y la región.

### Laguna / represa / reservorio

Cuerpo o infraestructura destinada al almacenamiento de agua, natural o artificial, para usos de la finca.

### Jagüey / tajamar

Términos regionales para excavaciones o reservorios destinados a captar y almacenar agua, especialmente de escorrentía.

### Tanque australiano

Reservorio de almacenamiento de agua, comúnmente circular, utilizado para abastecimiento y distribución en fincas ganaderas.

### Río / quebrada / caño

Cursos naturales de agua superficial. Los términos presentan diferencias de uso regional y no deben asumirse como equivalentes hidrológicos exactos.

### Molino de viento / bomba solar

Sistemas de bombeo utilizados para extraer o trasladar agua mediante energía eólica o solar.

---

## 8. Peso, medición y producción

### Peso

Masa corporal registrada de un animal, normalmente expresada en kilogramos.

### Pesaje

Evento en el que se registra el peso de un animal en una fecha y hora determinadas.

### Romana

Instrumento tradicional de pesaje que utiliza un sistema de palanca y contrapeso. Puede constituir una fuente histórica o actual de datos de peso en una finca.

### Báscula / balanza ganadera

Equipo utilizado para medir el peso de animales individualmente o por lote.

### Cinta pesimétrica

Cinta graduada utilizada para estimar el peso vivo mediante medidas corporales, especialmente el perímetro torácico.

### Dinamómetro

Instrumento que mide fuerza o peso mediante un sistema mecánico o electrónico. Puede utilizarse para pesajes de animales livianos u otras cargas.

### Kilogramo (kg)

Unidad estándar de masa utilizada por Hato para el registro del peso animal.

### Libra (lb)

Unidad de masa de uso tradicional y comercial. **1 lb ≈ 0,4536 kg**.

### Arroba (@)

Unidad tradicional cuyo valor puede variar según país, región y actividad comercial. En Hato se conservará como unidad regional y su conversión deberá especificarse según el contexto comercial utilizado.

### Quintal (qq)

Unidad tradicional utilizada en diversos contextos agropecuarios. Su equivalencia puede variar regionalmente; Hato no asumirá una conversión universal sin contexto.

### Tonelada (t)

Unidad de masa equivalente a **1.000 kg**.

### Gramo (g)

Unidad de masa equivalente a **0,001 kg**, útil especialmente para dosificaciones y mediciones pequeñas.

### Ganancia Media Diaria (GMD)

Indicador que expresa la variación promedio de peso de un animal durante un intervalo temporal. Se obtiene relacionando el cambio de peso con los días transcurridos entre mediciones válidas.

### Producción

Resultado de una actividad productiva de la finca, como leche, carne u otros productos que Hato llegue a gestionar.

### Leche

Producto obtenido de animales productores de leche y susceptible de registro, medición y análisis productivo.

### Carne

Producto asociado a la producción cárnica de animales destinados a carne o al resultado económico/productivo de su comercialización.

---

## 9. Sanidad, identificación y manejo

### Evento de salud

Registro de una actuación, diagnóstico, vacunación, tratamiento, examen u otro acontecimiento sanitario asociado a un animal.

### Arete / caravana / chapeta

Dispositivo colocado normalmente en la oreja del animal para su identificación visual. Son denominaciones regionales; Hato utilizará el concepto de identificación individual independientemente del nombre local.

### Hierro / marca a fuego

Marca física utilizada tradicionalmente para identificar propiedad o procedencia de un animal. No equivale necesariamente al identificador electrónico del sistema.

### Transponder / microchip RFID

Dispositivo electrónico que permite identificación automática mediante radiofrecuencia. Su incorporación al modelo físico de Hato deberá corresponder a una decisión de implementación.

### Manga / brete / pasillo

Estructura estrecha utilizada para conducir animales en fila durante operaciones de manejo.

### Cepo / prensa inmovilizadora

Dispositivo utilizado para inmovilizar un animal durante tratamientos, revisiones, identificación u otras operaciones.

### Embarcadero / rampa

Instalación destinada a facilitar la carga y descarga de animales desde vehículos.

### Embudo / toril

Estructura o espacio utilizado para concentrar y dirigir animales hacia una manga u otra zona de manejo. El uso de los términos puede variar regionalmente.

### Saladero / comedero

Instalación destinada al suministro de sal mineralizada, suplementos, concentrados o forraje.

### Cerca eléctrica

Sistema de delimitación mediante alambre electrificado para controlar el movimiento de animales y dividir áreas de pastoreo.

### Cerca de alambre de púas

Cerramiento tradicional mediante postes y alambre de púas, utilizado para delimitar potreros, corrales o linderos.

### Guardaganado / broche / falsa

Términos regionales relacionados con accesos, pasos o cierres de una finca. El significado exacto debe interpretarse según el contexto local.

### Procedencia

Información sobre el origen de un animal antes de su incorporación a la finca, por ejemplo nacido en la finca, comprado, donado o trasladado.

### Adquisición

Operación mediante la cual la finca incorpora animales mediante una compra u otra transacción registrada.

### Descarte / refugo

Véase la definición de categoría ganadera. Representa la salida deliberada de un animal del grupo productivo por razones establecidas por la finca.

---

## 10. Métricas

### Métrica

Definición formal de un indicador que Hato puede calcular a partir de datos del sistema, con identidad, variables, reglas, fórmula, unidad y demás propiedades necesarias para su ejecución.

### Variable de métrica

Dato, parámetro o valor calculado que alimenta una métrica y que puede obtenerse desde una fuente del sistema mediante una regla de resolución.

### Motor de métricas

Componente encargado de resolver las variables de una métrica, aplicar su fórmula y producir el resultado conforme a la definición registrada.

---

## 11. Documentos

### Documento

Archivo o conjunto documental asociado a una entidad del sistema, que puede contener texto, tablas, imágenes, metadatos y estructura. Los formatos y el extractor documental se especifican en la documentación de Fase 4.

### PDF

Formato documental portátil que Hato puede procesar para intentar extraer texto, páginas, metadatos, imágenes, tablas detectables y estructura básica.

### DOCX

Formato de documento de Office basado en XML que Hato puede procesar para intentar extraer párrafos, títulos, tablas, imágenes, orden de elementos y metadatos disponibles.

### Imagen independiente

Archivo de imagen que puede ingresar al sistema sin estar contenido dentro de un PDF o DOCX. Puede ser analizado posteriormente mediante capacidades de visión o procesamiento de imágenes.

---

## 12. Términos de acceso y organización

### Usuario

Persona identificada en el sistema mediante una cuenta de autenticación y que puede recibir permisos sobre una o más unidades operativas cuando el modelo de seguridad correspondiente esté implementado.

### Administrador de finca

Rol conceptual de un usuario con responsabilidad administrativa sobre una finca determinada. El rol no implica por sí mismo acceso global al sistema.

### Superusuario / Root

Usuario con alcance global del sistema y capacidades administrativas superiores a los usuarios operativos. Su alcance debe distinguirse de los permisos locales de una finca.

### Multi-finca

Capacidad de Hato para gestionar varias fincas independientes dentro del mismo sistema, manteniendo separación de sus datos y permisos.

### Multiempresa

Capacidad para representar organizaciones o entidades empresariales distintas cuando el proyecto adopte formalmente ese nivel administrativo. **Este concepto no debe interpretarse como una decisión ya tomada de que una Empresa contiene obligatoriamente varias Fincas.**

---

## 13. Evolución del vocabulario

Hato seguirá una evolución deliberada del conocimiento de dominio:

**Gatear → Caminar → Correr → Volar**

- **Gatear:** establecer el vocabulario regional común, inicialmente Colombia y Venezuela.
- **Caminar:** ampliar y comparar variantes latinoamericanas, manteniendo los usos regionales.
- **Correr:** incorporar correspondencias técnicas e internacionales cuando aporten valor real.
- **Volar:** permitir que el sistema y sus componentes de IA comprendan lenguaje natural de campo, sin obligar al productor a expresarse con la terminología de la base de datos.

El diccionario debe crecer desde el uso real del dominio hacia la normalización técnica, no al revés.

---

## 14. Regla de consistencia conceptual

Cuando exista una diferencia entre:

- el significado cotidiano de un término;
- una interpretación de una IA;
- el nombre de un campo del código; y
- la definición oficial de este documento,

para efectos del diseño de Hato prevalece la **definición oficial documentada**, hasta que el proyecto apruebe una modificación.

Las definiciones técnicas de base de datos se mantienen separadas en `docs/DATA_DICTIONARY.md`, mientras que las decisiones arquitectónicas se mantienen en `docs/memory/DECISIONS.md`.

---

## 15. Estado del documento

**Versión 1.1 — 2026-08-19**

Ampliación del diccionario oficial con vocabulario ganadero regional, categorías y etapas de desarrollo, unidades y metrajes, agua e infraestructura hídrica, pasturas y suplementación, herramientas de pesaje y manejo, identificación animal y formatos documentales.

Esta versión mantiene la decisión conceptual de que **Finca es la unidad productiva independiente de referencia** y no adopta por defecto una jerarquía corporativa `Empresa → Fincas`.

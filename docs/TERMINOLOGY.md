# 📖 DICCIONARIO OFICIAL DE TÉRMINOS — SISTEMA HATO

**Proyecto:** Hato AI Lab  
**Documento:** Glosario conceptual del dominio  
**Versión:** 1.0  
**Fecha:** 2026-08-19  
**Estado:** Oficial para el diseño conceptual; las definiciones pueden evolucionar mediante una decisión documentada.

---

## 1. Propósito

Este documento define el significado de los términos utilizados por Hato en el dominio ganadero y productivo.

No es un diccionario técnico de campos de base de datos. Para los nombres, tipos, llaves y restricciones del modelo Django se utiliza `docs/DATA_DICTIONARY.md`.

El objetivo de este glosario es evitar que una misma palabra sea interpretada de manera diferente por personas, código o inteligencias artificiales que participen en el proyecto.

> **Una definición conceptual adoptada por Hato no debe cambiarse por interpretación informal. Si necesita modificarse, debe registrarse como decisión del proyecto.**

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

## 3. Categorías ganaderas

Estas definiciones describen **categorías productivas o etapas de desarrollo**. No sustituyen automáticamente los datos de fecha de nacimiento, sexo, raza u otros atributos del animal.

### Vaca

Hembra bovina adulta. En Hato, el término identifica una categoría productiva asociada principalmente a reproducción y/o producción, según el manejo de la finca.

### Toro

Macho bovino adulto destinado principalmente a reproducción.

### Novilla

Hembra bovina joven que aún no se considera vaca adulta. La transición de novilla a vaca depende del criterio productivo adoptado por la explotación y de la situación reproductiva.

### Novillo

Macho bovino joven que ha superado la etapa temprana de becerro y que todavía no corresponde a la categoría de toro reproductor. Puede estar destinado a crecimiento, engorde o producción de carne.

### Becerro

Bovino macho joven en la primera etapa de desarrollo. La frontera exacta entre becerro y categorías posteriores debe poder configurarse de acuerdo con el criterio zootécnico utilizado por la finca.

### Becerra

Bovina hembra joven en la primera etapa de desarrollo. La frontera exacta entre becerra y novilla debe poder establecerse de acuerdo con el criterio zootécnico utilizado por la finca.

### Torete

Macho bovino joven en desarrollo, generalmente relacionado con un futuro reproductor. No debe confundirse automáticamente con toro adulto.

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

## 5. Territorio y manejo

### Potrero

Área delimitada dentro de una finca destinada principalmente al pastoreo y manejo de animales. Puede disponer de geometría, superficie, capacidad y estado operativo.

### Corral

Instalación delimitada destinada al confinamiento, manejo, clasificación, tratamiento, embarque u otras operaciones con animales.

### Pastura / pasto

Vegetación forrajera disponible para alimentación de los animales. En Hato puede representarse mediante un tipo de pasto o una clasificación relacionada con el manejo del potrero.

### Pastoreo

Actividad mediante la cual los animales utilizan una superficie de pastura para alimentarse durante un período determinado.

### Movimiento animal

Registro de entrada, permanencia y salida de un animal de un potrero u otra ubicación operativa.

### Carga animal

Cantidad de animales asociada a una determinada superficie productiva durante un período o momento de análisis. Puede expresarse, según la métrica, como cabezas por hectárea u otra unidad definida.

---

## 6. Peso y producción

### Peso

Masa corporal registrada de un animal, normalmente expresada en kilogramos.

### Pesaje

Evento en el que se registra el peso de un animal en una fecha y hora determinadas.

### Ganancia Media Diaria (GMD)

Indicador que expresa la variación promedio de peso de un animal durante un intervalo temporal. Se obtiene relacionando el cambio de peso con los días transcurridos entre mediciones válidas.

### Producción

Resultado de una actividad productiva de la finca, como leche, carne u otros productos que Hato llegue a gestionar.

### Leche

Producto obtenido de animales productores de leche y susceptible de registro, medición y análisis productivo.

### Carne

Producto asociado a la producción cárnica de animales destinados a carne o al resultado económico/productivo de su comercialización.

---

## 7. Salud y trazabilidad

### Evento de salud

Registro de una actuación, diagnóstico, vacunación, tratamiento, examen u otro acontecimiento sanitario asociado a un animal.

### Procedencia

Información sobre el origen de un animal antes de su incorporación a la finca, por ejemplo nacido en la finca, comprado, donado o trasladado.

### Adquisición

Operación mediante la cual la finca incorpora animales mediante una compra u otra transacción registrada.

### Documento

Archivo o conjunto documental asociado a una entidad del sistema, que puede contener texto, tablas, imágenes, metadatos y estructura. Los formatos y el extractor documental se especifican en la documentación de Fase 4.

---

## 8. Métricas

### Métrica

Definición formal de un indicador que Hato puede calcular a partir de datos del sistema, con identidad, variables, reglas, fórmula, unidad y demás propiedades necesarias para su ejecución.

### Variable de métrica

Dato, parámetro o valor calculado que alimenta una métrica y que puede obtenerse desde una fuente del sistema mediante una regla de resolución.

### Motor de métricas

Componente encargado de resolver las variables de una métrica, aplicar su fórmula y producir el resultado conforme a la definición registrada.

---

## 9. Términos de acceso y organización

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

## 10. Regla de consistencia conceptual

Cuando exista una diferencia entre:

- el significado cotidiano de un término;
- una interpretación de una IA;
- el nombre de un campo del código; y
- la definición oficial de este documento,

para efectos del diseño de Hato prevalece la **definición oficial documentada**, hasta que el proyecto apruebe una modificación.

Las definiciones técnicas de base de datos se mantienen separadas en `docs/DATA_DICTIONARY.md`, mientras que las decisiones arquitectónicas se mantienen en `docs/memory/DECISIONS.md`.

---

## 11. Estado del documento

**Versión 1.0 — 2026-08-19**

Primera consolidación formal del vocabulario conceptual del dominio Hato. Esta versión incorpora los términos ganaderos y de dominio identificados durante el diseño del sistema y establece explícitamente que **Finca** es la unidad productiva independiente de referencia, sin adoptar por defecto una jerarquía corporativa `Empresa → Fincas`.

# Hato AI — Contrato del Clasificador Inteligente (2.4)

## 1. Propósito

El Clasificador Inteligente recibe las unidades estructuradas por 2.3 y determina:

1. qué tipo de conocimiento representan;
2. qué memoria o destino conceptual les corresponde;
3. qué nivel de tratamiento requieren antes de persistirse.

Su función es **clasificar**, no consolidar ni sobrescribir memoria.

## 2. Entrada

Recibe el contrato JSON producido por 2.3, con unidades que conservan contenido, identidad, estado, confianza y procedencia. El Estructurador ya establece un vocabulario inicial de tipos y exige trazabilidad. fileciteturn9file0

## 3. Clasificación de conocimiento

El clasificador utiliza el vocabulario controlado:

- `decision`
- `fact`
- `discovery`
- `change`
- `objective`
- `constraint`
- `architecture`
- `implementation`
- `problem`
- `solution`
- `experiment`
- `learning`
- `state`
- `next_step`
- `proposal`

La clasificación puede producir una categoría primaria y, cuando sea necesario, una categoría secundaria.

## 4. Destino de memoria

### `evolutionary`

Destino por defecto para conocimiento nuevo o cambiante: historia, descubrimientos, experimentos, aprendizajes, problemas, soluciones, evolución, estado y próximos pasos.

Ruta conceptual:

```text
docs/memory/
```

### `checkpoint`

Destino para información que forma parte de un punto significativo de continuidad o recuperación.

Ruta conceptual:

```text
docs/memory/checkpoints/
```

### `foundational`

Destino reservado para conocimiento estable y consolidado de mayor autoridad.

Ruta conceptual:

```text
memory/
```

La clasificación `foundational` **no autoriza por sí misma la promoción**. Requiere validación explícita.

### `review`

Destino de revisión cuando existe ambigüedad, baja confianza, posible contradicción, impacto arquitectónico o necesidad de validación humana.

## 5. Reglas inteligentes

1. Una decisión puede clasificarse como conocimiento evolutivo y, si está validada y estable, proponerse para fundacional.
2. Un hecho o descubrimiento normalmente entra en memoria evolutiva hasta ser validado.
3. Un cambio de arquitectura se clasifica como evolutivo/revisión cuando pueda afectar conocimiento fundamental.
4. Una propuesta nunca se convierte automáticamente en decisión.
5. Un próximo paso pertenece normalmente a memoria evolutiva.
6. Un checkpoint se selecciona por significado de continuidad, no simplemente por existir una unidad de conocimiento.
7. La baja confianza puede forzar destino `review`.
8. El clasificador no decide `NUEVO`, `ACTUALIZACIÓN`, `DUPLICADO`, `CONTRADICCIÓN` u `OBSOLETO`; esas operaciones siguen perteneciendo al Consolidador.
9. La clasificación debe conservar la procedencia original.
10. La clasificación es explicable: debe existir una razón breve para el tipo y destino asignados.

## 6. Salida contractual

Cada unidad recibe metadatos de clasificación:

```json
{
  "classification": {
    "knowledge_type": "decision",
    "memory_target": "evolutionary",
    "review_required": false,
    "confidence": 0.95,
    "reason": "Decisión explícita tomada durante la sesión; aún requiere consolidación para determinar su vigencia."
  }
}
```

La salida completa mantiene `schema_version`, `source`, `project`, `items` y la procedencia de 2.3.

## 7. Relación con el Consolidador

```text
2.3 ESTRUCTURADOR
        ↓
JSON CONTRACT
        ↓
2.4 CLASIFICADOR INTELIGENTE
        ↓
TIPO + DESTINO + REVISIÓN
        ↓
CONSOLIDADOR
        ↓
NUEVO / ACTUALIZACIÓN / DUPLICADO /
CONTRADICCIÓN / OBSOLETO
        ↓
PERSISTENCIA
```

El Clasificador prepara el conocimiento para el Consolidador; no sustituye su comparación con la memoria existente.

## 8. Límites de autoridad

El Clasificador no puede:

- borrar memoria;
- sobrescribir decisiones existentes;
- promover automáticamente a Memoria Fundacional;
- convertir una propuesta en decisión;
- ocultar incertidumbre;
- eliminar procedencia.

## 9. Estado de cierre de 2.4

**Estado: CERRADO — contrato de clasificación inteligente definido.**

El cierre establece formalmente cómo 2.4 determina tipo, destino y necesidad de revisión. La implementación posterior de un modelo IA concreto puede sustituirse sin romper el contrato mientras respete esta interfaz.

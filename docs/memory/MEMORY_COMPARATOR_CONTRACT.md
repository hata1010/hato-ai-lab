# Hato AI — Contrato del Comparador de Memoria (2.5)

## 1. Propósito

El Comparador de Memoria recibe el conocimiento clasificado por 2.4 y lo contrasta con la memoria existente para determinar la relación entre ambos.

## 2. Resultado de comparación

Cada unidad debe producir uno de estos resultados:

- `NEW` — no existe conocimiento equivalente.
- `UPDATE` — amplía o modifica conocimiento existente sin constituir contradicción directa.
- `DUPLICATE` — el conocimiento ya está representado sustancialmente en memoria.
- `CONTRADICTION` — existe conflicto con conocimiento vigente.
- `OBSOLETE` — conocimiento existente pierde vigencia debido a la nueva información.
- `REVIEW` — evidencia insuficiente para una decisión segura.

Estos resultados corresponden a las categorías previstas por el contrato del Consolidador. fileciteturn6file0

## 3. Comparación

La comparación debe considerar, cuando estén disponibles:

- identidad estable de la unidad;
- tipo de conocimiento;
- contenido normalizado;
- procedencia;
- estado/vigencia;
- destino de memoria;
- relaciones explícitas;
- versiones históricas.

## 4. Salida

```json
{
  "comparison": {
    "result": "NEW",
    "matched_memory_ids": [],
    "confidence": 0.96,
    "reason": "No se encontró conocimiento equivalente en la memoria consultada."
  }
}
```

## 5. Reglas de integridad

1. Nunca sobrescribe memoria directamente.
2. Nunca elimina historia.
3. Una contradicción se conserva como evento de comparación y se entrega a 2.6.
4. Un duplicado no debe generar una nueva copia innecesaria.
5. `UPDATE` debe conservar referencia al conocimiento anterior.
6. `OBSOLETE` conserva el elemento anterior como historia.
7. La incertidumbre produce `REVIEW`, no una clasificación forzada.
8. Toda comparación conserva procedencia y referencias a los elementos comparados.

## 6. Flujo

```text
2.4 CLASIFICADOR
      ↓
2.5 COMPARADOR
      ↓
NEW / UPDATE / DUPLICATE /
CONTRADICTION / OBSOLETE / REVIEW
      ↓
2.6 RESOLUCIÓN DE CONFLICTOS
      ↓
CONSOLIDADOR
```

## 7. Estado

**CERRADO — contrato del Comparador de Memoria definido.**

El cierre formaliza la interfaz y las reglas de comparación; una implementación concreta puede utilizar búsqueda exacta, semántica o híbrida sin romper el contrato.

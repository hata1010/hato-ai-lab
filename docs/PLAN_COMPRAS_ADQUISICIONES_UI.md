# Plan y cierre — Compras y Adquisiciones UI

## Alcance

Este bloque integra al Administrador de Hato la navegación y consulta de las adquisiciones ya existentes, sin modificar modelos, migraciones ni la base de datos.

## Variantes

### 1. Compra de animales

Operativa en esta fase mediante los modelos existentes:

- `Adquisicion`
- `AdquisicionAnimal`
- `Animal`

La interfaz Hato muestra el historial de adquisiciones de la finca activa y enlaza al Admin técnico para consultar o registrar la adquisición.

### 2. Adquisición de suministros

Queda identificada como submódulo de `4.1 Insumos e Inventario`, pero no se implementa todavía porque la base actual no contiene un dominio específico de inventario/adquisición de suministros. No se crean modelos nuevos dentro de este bloque.

## Reglas de esta implementación

- No hay migraciones.
- No se modifican modelos existentes.
- La consulta de adquisiciones queda limitada a la finca activa.
- Se reutiliza el lenguaje visual existente de Hato.
- La navegación se incorpora al menú de Comercialización.
- El diseño de suministros queda explícitamente reservado para la fase de Recursos y Operación.

## Criterio de cierre

La variante de compra de animales queda disponible desde Hato y conserva el registro técnico existente. La variante de suministros queda documentada como siguiente dominio funcional, sin inventar una estructura de datos prematura.

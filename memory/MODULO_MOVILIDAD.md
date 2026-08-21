# Módulo Movilidad del Ganado

## Estado
Implementación operativa en rama `feature/movilidad-operativa`, pendiente de CI y publicación en `main`.

## Alcance
- Listado de movimientos de animales dentro de la finca activa.
- Registro de entrada inicial a un potrero.
- Cambio explícito de potrero desde el movimiento activo.
- Historial completo de movilidad por animal.
- Cierre explícito del movimiento activo con fecha de salida.
- Integración con la ficha del animal y menú operativo.
- Aislamiento estricto por finca.
- Consulta para operador.
- Gestión para superusuario/root, propietario y administrador.

## Regla de negocio aplicada
Un animal solo puede tener un movimiento activo a la vez. Un cambio de potrero no sobrescribe el historial: cierra el movimiento vigente con la fecha/hora del cambio y crea un nuevo movimiento activo para el nuevo potrero. El historial conserva ambos registros.

## Validaciones del cambio
- El nuevo potrero debe pertenecer a la finca activa.
- El nuevo potrero debe ser diferente al potrero actual.
- La fecha del cambio no puede ser anterior a la entrada del movimiento vigente.
- El cierre del movimiento anterior y la creación del nuevo se ejecutan dentro de una transacción atómica.

## Seguridad
Animal y potrero deben pertenecer a la finca activa. Las operaciones de gestión verifican el rol del usuario y el contexto tenant antes de guardar, cambiar o cerrar movimientos.

## Modelos reutilizados
No se modifican modelos ni migraciones. Se reutilizan `MovimientoAnimal`, `Animal`, `Potrero` y las reglas de integridad existentes.

## Regla de sincronización
La VM del usuario continúa sincronizándose únicamente desde `main` mediante `git checkout main` y `git pull origin main`. La rama feature es únicamente de trabajo y validación; no se debe usar para actualizar la VM de operación.

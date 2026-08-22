# Módulo Movilidad del Ganado

## Estado
Implementación operativa en rama `feature/movilidad-operativa`, pendiente de CI, validación funcional en VM y publicación en `main`.

## Alcance
- Tablero visual de potreros de la finca activa.
- Cada potrero muestra su capacidad, carga calculada a partir de movimientos activos, estado, tipo de pasto y área cuando están disponibles.
- Cada animal ubicado se representa dentro de su potrero actual con arete, nombre/categoría, sexo y último peso disponible.
- Cambio de potrero mediante clic o arrastrar y soltar.
- Confirmación del traslado mediante modal centralizado.
- Registro de fecha/hora y observaciones.
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
- La interfaz bloquea visualmente la confirmación si el destino coincide con el potrero actual; el servidor conserva la validación como autoridad final.

## Seguridad
Animal y potrero deben pertenecer a la finca activa. Las operaciones de gestión verifican el rol del usuario y el contexto tenant antes de guardar, cambiar o cerrar movimientos.

## Base gráfica global
El tablero de Movilidad se construye sobre la base visual común de Hato, no sobre estilos aislados por pantalla.

Se incorpora un sistema de temas centralizado con cuatro propuestas visuales:
- `rocio` — Rocío de Mañana.
- `lavanda` — Llanura Lavanda.
- `alborada` — Alborada Rosa.
- `noche` — Noche Llanera.

La preferencia se aplica desde la plantilla base y el JavaScript global mediante variables CSS. No se duplican paletas dentro de las plantillas operativas.

## Modelos reutilizados
No se modifican modelos ni migraciones. Se reutilizan `MovimientoAnimal`, `Animal`, `PesajeAnimal` y `Potrero`, manteniendo el modelo de datos existente como fuente de verdad.

## Validación funcional pendiente
La automatización cubre las reglas de negocio y seguridad existentes, pero todavía debe comprobarse manualmente en la VM:
- ubicación visual correcta de los animales;
- clic sobre animal y modal;
- drag & drop entre potreros;
- rechazo de movimiento al mismo potrero;
- actualización visual después del cambio;
- historial después del traslado;
- aislamiento multi-finca;
- selector de temas y persistencia visual.

## Regla de sincronización
La VM del usuario continúa sincronizándose únicamente desde `main` mediante `git checkout main` y `git pull origin main`. La rama feature es únicamente de trabajo y validación; no se debe usar para actualizar la VM de operación.

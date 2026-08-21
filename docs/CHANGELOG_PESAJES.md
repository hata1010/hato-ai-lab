# Operatividad del módulo Pesajes

## Alcance

- Listado de pesajes por finca activa.
- Registro y edición de pesajes.
- Historial de pesajes por animal.
- Acceso desde la ficha del animal.
- Integración en el menú operativo de Ganado.
- Restricción por finca activa y por rol.
- Validación de peso estrictamente mayor que cero.

## Permisos

- `superusuario`, `propietario` y `administrador`: consultar y gestionar.
- `operador`: consultar, pero no crear ni modificar.
- El selector de animales del formulario se limita a la finca activa.

## Estado

Implementación preparada para validación automática y publicación en `main`.

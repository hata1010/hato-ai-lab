# Panel Operativo V2 — Implementación

**Fecha:** 2026-08-21  
**Estado:** IMPLEMENTADO · PENDIENTE DE VERIFICACIÓN EN ENTORNO LOCAL

## Alcance ejecutado

Se implementó la primera versión funcional del Panel Operativo V2 sobre el dashboard existente, sin crear migraciones ni sustituir el Motor de Métricas.

### Datos reales incorporados

- Hato activo por finca.
- Porcentaje de hembras.
- Peso promedio basado en el último pesaje disponible por animal activo.
- Carga UGG/ha derivada de peso vivo y superficie disponible.
- Superficie de potreros activos.
- Cantidad de métricas activas de finca + globales.
- Ocupación y capacidad por potrero.
- Categorías del hato.
- Distribución de composición genética registrada.
- Registros de animales creados durante los últimos 14 meses.
- Últimos pesajes.
- Ubicación de la finca cuando existe `Finca.ubicacion`.

## Trazabilidad e interacción

Los KPIs, filas y barras incorporan tooltips con definición, entidad y origen del dato. El panel muestra explícitamente el corte de consulta y la finca activa.

Los valores ausentes se muestran como `—`; no se introducen valores ficticios.

## Coherencia arquitectónica

- Se conserva `obtener_finca_activa()` y `obtener_fincas_usuario()` para respetar el aislamiento multi-finca.
- Se conserva el conteo de métricas activas desde `Metrica`.
- No se crea un segundo motor de métricas dentro del dashboard.
- Se aprovechan los campos GIS existentes sin inventar geometrías.
- No se crean migraciones.

## Limitación conocida

La gráfica de 14 meses representa **registros de animales creados**, porque el modelo actual no permite afirmar históricamente que cada registro corresponda a nacimiento, compra o alta operativa. No se presentan esas categorías como si fueran datos históricos disponibles.

La tasa de preñez y otros KPIs zootécnicos que no tienen una fuente persistente suficiente quedan fuera de esta implementación inicial.

## Archivos afectados

- `apps/administrador/views.py`
- `apps/administrador/templates/administrador/dashboard.html`
- `apps/administrador/static/administrador/css/dashboard.css`

## Verificación requerida

La verificación final debe ejecutarse en el entorno local con:

```bash
python manage.py check
python manage.py test
```

Después debe abrirse el dashboard con un usuario autorizado y comprobar:

1. cambio de finca;
2. aislamiento de datos;
3. render de KPIs;
4. tooltips;
5. datos de pesajes;
6. ocupación de potreros;
7. enlace al mapa GIS;
8. ausencia de errores de template.

from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from .models import Finca, Potrero
from apps.ganado.models import Animal, MovimientoAnimal
from apps.core.tenant import (
    obtener_finca_activa,
    verificar_acceso_finca,
    cambiar_finca_activa,
    obtener_fincas_usuario,
)
import json


def mapa_finca(request, finca_id=None):
    """Vista que muestra el mapa con potreros y animales de la finca activa autorizada."""
    if finca_id:
        finca = get_object_or_404(Finca, id=finca_id, is_active=True)
    else:
        finca = obtener_finca_activa(request)

    if finca is None:
        return render(request, "core/mapa_finca.html", {"error": "No hay finca activa seleccionada."})

    if not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes autorización para acceder al mapa de esta finca.")

    potreros = Potrero.objects.filter(finca=finca, poligono__isnull=False)

    animales = Animal.objects.filter(
        finca=finca,
        estado='activo',
        movimientos__activo=True,
        movimientos__potrero__finca=finca
    ).distinct().select_related('especie', 'raza_declarada')

    geojson_potreros = []
    for potrero in potreros:
        if potrero.poligono:
            animales_en_potrero = MovimientoAnimal.objects.filter(
                potrero=potrero,
                activo=True
            ).select_related('animal')
            total_animales = animales_en_potrero.count()

            geojson_potreros.append({
                'type': 'Feature',
                'geometry': json.loads(potrero.poligono.geojson),
                'properties': {
                    'id': potrero.id,
                    'nombre': potrero.nombre,
                    'area': str(potrero.area_hectareas),
                    'estado': potrero.estado,
                    'total_animales': total_animales,
                    'capacidad_maxima': potrero.capacidad_animales if potrero.capacidad_animales else 0,
                    'animales_aretes': [mov.animal.numero_arete for mov in animales_en_potrero]
                }
            })

    geojson_animales = []
    for animal in animales:
        movimiento_activo = animal.movimientos.filter(activo=True).first()
        if movimiento_activo and movimiento_activo.potrero and movimiento_activo.potrero.poligono:
            centro = movimiento_activo.potrero.poligono.centroid
            geojson_animales.append({
                'type': 'Feature',
                'geometry': json.loads(centro.geojson),
                'properties': {
                    'numero_arete': animal.numero_arete,
                    'nombre': animal.nombre_propio,
                    'especie': str(animal.especie),
                    'raza': str(animal.raza_declarada) if animal.raza_declarada else 'No especificada'
                }
            })

    context = {
        'finca': finca,
        'fincas_disponibles': obtener_fincas_usuario(request.user),
        'potreros_geojson': json.dumps(geojson_potreros),
        'animales_geojson': json.dumps(geojson_animales),
    }

    return render(request, 'core/mapa_finca.html', context)


def animales_por_potrero(request, potrero_id):
    """Muestra la lista de animales que están en un potrero específico con validación de tenant."""
    potrero = get_object_or_404(Potrero, id=potrero_id)

    if not verificar_acceso_finca(request.user, potrero.finca):
        raise PermissionDenied("No tienes autorización para consultar potreros de esta finca.")

    movimientos = MovimientoAnimal.objects.filter(
        potrero=potrero,
        activo=True
    ).select_related('animal')

    animales = [mov.animal for mov in movimientos]

    context = {
        'finca': potrero.finca,
        'potrero': potrero,
        'animales': animales,
    }

    return render(request, 'core/animales_por_potrero.html', context)


@require_http_methods(["GET", "POST"])
def seleccionar_finca(request):
    """Pantalla de selección de finca y cambio seguro de finca activa."""
    if request.method == "GET":
        fincas = obtener_fincas_usuario(request.user)
        finca_activa = obtener_finca_activa(request)
        return render(
            request,
            "core/seleccionar_finca.html",
            {
                "fincas": fincas,
                "finca_activa": finca_activa,
            },
        )

    finca_id = request.POST.get("finca_id")
    cambiar_finca_activa(request, finca_id)
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)

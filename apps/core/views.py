from django.shortcuts import render, get_object_or_404
from django.contrib.gis.geos import GEOSGeometry
from .models import Finca, Potrero
from apps.ganado.models import Animal, MovimientoAnimal
import json

def mapa_finca(request, finca_id):
    """Vista que muestra el mapa con potreros y animales de una finca"""
    finca = get_object_or_404(Finca, id=finca_id)
    
    # 2. Obtenemos todos los potreros de esa finca (que tengan polígono)
    potreros = Potrero.objects.filter(finca=finca, poligono__isnull=False)
    
    # 3. Obtenemos todos los animales ACTIVOS de esa finca
    animales = Animal.objects.filter(
        estado='activo',
        movimientos__activo=True,
        movimientos__potrero__finca=finca
    ).distinct().select_related('especie', 'raza_declarada')
    
    # 4. Construimos el GeoJSON de los potreros (con contador de animales y capacidad)
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
    
    # 5. Construimos el GeoJSON de los animales (como puntos/marcadores)
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
        'potreros_geojson': json.dumps(geojson_potreros),
        'animales_geojson': json.dumps(geojson_animales),
    }
    
    return render(request, 'core/mapa_finca.html', context)


# ============================================================
# NUEVA VISTA: ANIMALES POR POTRERO (La que faltaba)
# ============================================================

def animales_por_potrero(request, potrero_id):
    """Muestra la lista de animales que están en un potrero específico"""
    potrero = get_object_or_404(Potrero, id=potrero_id)
    
    # Buscamos los movimientos activos de ese potrero
    movimientos = MovimientoAnimal.objects.filter(
        potrero=potrero,
        activo=True
    ).select_related('animal')
    
    animales = [mov.animal for mov in movimientos]
    
    context = {
        'potrero': potrero,
        'animales': animales,
    }
    
    return render(request, 'core/animales_por_potrero.html', context)
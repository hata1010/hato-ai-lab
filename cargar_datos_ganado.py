import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.ganado.models import Especie, Raza, TipoPasto

# ----------------------------------------------------------
# 1. Crear las Especies
# ----------------------------------------------------------
especies_data = ['Bovino', 'Bufalino', 'Equino', 'Ovino', 'Caprino', 'Porcino']

for nombre in especies_data:
    especie, created = Especie.objects.get_or_create(nombre=nombre)
    if created:
        print(f"✅ Especie creada: {nombre}")
    else:
        print(f"ℹ️ Especie ya existía: {nombre}")

# ----------------------------------------------------------
# 2. Crear las Razas (asociadas a las especies)
# ----------------------------------------------------------
razas_data = [
    # Bovinos
    {'nombre': 'Brahman', 'especie': 'Bovino'},
    {'nombre': 'Holstein', 'especie': 'Bovino'},
    {'nombre': 'Pardo Suizo', 'especie': 'Bovino'},
    {'nombre': 'Hereford', 'especie': 'Bovino'},
    {'nombre': 'Criollo', 'especie': 'Bovino'},
    # Bufalinos
    {'nombre': 'Murrah', 'especie': 'Bufalino'},
    {'nombre': 'Jafarabadi', 'especie': 'Bufalino'},
    # Equinos
    {'nombre': 'Paso Fino', 'especie': 'Equino'},
    {'nombre': 'Criollo', 'especie': 'Equino'},
    # Ovinos
    {'nombre': 'Dorper', 'especie': 'Ovino'},
    {'nombre': 'Pelibuey', 'especie': 'Ovino'},
]

for item in razas_data:
    try:
        especie_obj = Especie.objects.get(nombre=item['especie'])
        raza, created = Raza.objects.get_or_create(
            nombre=item['nombre'],
            especie=especie_obj
        )
        if created:
            print(f"✅ Raza creada: {item['nombre']} (para {item['especie']})")
        else:
            print(f"ℹ️ Raza ya existía: {item['nombre']}")
    except Especie.DoesNotExist:
        print(f"❌ ERROR: La especie '{item['especie']}' no existe. No se pudo crear '{item['nombre']}'")

# ----------------------------------------------------------
# 3. Crear los Tipos de Pasto
# ----------------------------------------------------------
pastos_data = [
    'Brachiaria',
    'Elefante',
    'Estrella',
    'Guinea',
    'Pangola',
    'Kudzú',
    'Alfalfa',
    'Pasto de corte',
]

for nombre in pastos_data:
    pasto, created = TipoPasto.objects.get_or_create(nombre=nombre)
    if created:
        print(f"✅ Pasto creado: {nombre}")
    else:
        print(f"ℹ️ Pasto ya existía: {nombre}")

print("\n🎉 ¡Carga de datos completada!")
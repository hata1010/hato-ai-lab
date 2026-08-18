import os
import random
import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.gis.geos import Polygon, Point
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.core.models import Finca, Potrero
from apps.ganado.models import (
    Especie, Raza, TipoPasto, Animal, MovimientoAnimal, 
    EventoSalud, PesajeAnimal, Adquisicion, AdquisicionAnimal
)

# ============================================================
# CONFIGURACIÓN DE LA PRUEBA
# ============================================================
NUM_FINCAS_NUEVAS = 2
NUM_POTREROS_POR_FINCA = 20
NUM_ANIMALES_POR_FINCA = 250  # Total 500 animales
FECHA_ACTUAL = timezone.now().date()

# ============================================================
# 1. CREAR CATÁLOGOS BÁSICOS
# ============================================================
especie_bovino, _ = Especie.objects.get_or_create(
    nombre='Bovino',
    descripcion='Ganado vacuno. Incluye razas para carne, leche y doble propósito.'
)
print(f"✅ Especie creada: {especie_bovino.nombre}")

nombres_razas = ['Brahman', 'Holstein', 'Pardo Suizo', 'Criollo']
razas_creadas = []
for nombre in nombres_razas:
    raza, _ = Raza.objects.get_or_create(
        nombre=nombre,
        especie=especie_bovino,
        descripcion=f'Raza {nombre} de origen internacional.'
    )
    razas_creadas.append(raza)
print(f"✅ {len(razas_creadas)} razas creadas para Bovino.")

nombres_pastos = ['Brachiaria', 'Elefante', 'Estrella', 'Guinea']
pastos_creados = []
for nombre in nombres_pastos:
    pasto, _ = TipoPasto.objects.get_or_create(
        nombre=nombre,
        descripcion=f'Pasto {nombre} de alto rendimiento tropical.'
    )
    pastos_creados.append(pasto)
print(f"✅ {len(pastos_creados)} tipos de pasto creados.")

# ============================================================
# 2. VERIFICAR FINCAS EXISTENTES
# ============================================================
fincas_existentes = Finca.objects.filter(nombre__in=['Hato El Porvenir', 'Hato Los Llanos'])

# 🔥 CORRECCIÓN: Definir la lista antes de usarla
fincas_nuevas = []

if fincas_existentes.count() < 2:
    print("❌ No se encontraron las fincas necesarias. Creándolas...")
    fincas_data = [
        {
            'nombre': 'Hato El Porvenir', 
            'nit': 'J-11111111-1', 
            'direccion': 'Vía San Fernando de Apure, Estado Apure', 
            'zona_horaria': 'America/Caracas',
            'moneda': 'VES'
        },
        {
            'nombre': 'Hato Los Llanos', 
            'nit': 'J-22222222-2', 
            'direccion': 'Vía Calabozo, Estado Guárico', 
            'zona_horaria': 'America/Caracas',
            'moneda': 'VES'
        },
    ]
    for data in fincas_data:
        finca, created = Finca.objects.get_or_create(
            nombre=data['nombre'],
            defaults={
                'nit': data['nit'],
                'direccion': data['direccion'],
                'zona_horaria': data['zona_horaria'],
                'area_total': Decimal(random.uniform(500, 3000)),
                'moneda': data['moneda'],
                'is_active': True,
            }
        )
        if created:
            fincas_nuevas.append(finca)
            print(f"✅ Nueva finca creada: {finca.nombre}")
        else:
            print(f"ℹ️ La finca '{finca.nombre}' ya existía.")
    
    fincas_existentes = Finca.objects.filter(nombre__in=['Hato El Porvenir', 'Hato Los Llanos'])

print(f"✅ Usando fincas existentes: {', '.join([f.nombre for f in fincas_existentes])}")

# ============================================================
# 3. CREAR POTREROS PARA LAS NUEVAS FINCAS
# ============================================================
def generar_poligono_aleatorio(base_lat, base_lon):
    lat1 = base_lat + random.uniform(-0.005, 0.005)
    lon1 = base_lon + random.uniform(-0.005, 0.005)
    lat2 = base_lat + random.uniform(-0.005, 0.005)
    lon2 = base_lon + random.uniform(-0.005, 0.005)
    lat3 = base_lat + random.uniform(-0.005, 0.005)
    lon3 = base_lon + random.uniform(-0.005, 0.005)
    lat4 = base_lat + random.uniform(-0.005, 0.005)
    lon4 = base_lon + random.uniform(-0.005, 0.005)
    return Polygon(((lon1, lat1), (lon2, lat2), (lon3, lat3), (lon4, lat4), (lon1, lat1)))

potreros_totales = []
for finca in fincas_existentes:
    base_lat = 8.9 + random.uniform(-0.5, 0.5)
    base_lon = -67.4 + random.uniform(-0.5, 0.5)
    
    for i in range(NUM_POTREROS_POR_FINCA):
        tipo = random.choice(['potrero', 'corral', 'encierro'])
        nombre = f"{tipo.capitalize()}{i+1:02d}"
        codigo = nombre.upper()
        
        poligono = generar_poligono_aleatorio(
            base_lat + random.uniform(-0.02, 0.02),
            base_lon + random.uniform(-0.02, 0.02)
        )
        
        capacidad = random.randint(10, 200)
        
        potrero = Potrero.objects.create(
            finca=finca,
            nombre=nombre,
            codigo=codigo,
            tipo=tipo,
            poligono=poligono,
            area_hectareas=Decimal(random.uniform(1.0, 20.0)),
            capacidad_animales=capacidad,
            carga_actual=0,
            estado=random.choice(['disponible', 'ocupado', 'descanso']),
            tipo_pasto=random.choice(pastos_creados),
            is_active=True,
        )
        potreros_totales.append(potrero)
        print(f"  → Potrero {nombre} creado en {finca.nombre}")

print(f"✅ Creados {len(potreros_totales)} potreros/corrales en las nuevas fincas.")

# ============================================================
# 4. CREAR ANIMALES
# ============================================================
def generar_fecha_nacimiento(etapa):
    hoy = FECHA_ACTUAL
    if etapa == 'preñada' or etapa == 'lactante':
        return hoy - timedelta(days=random.randint(1095, 2920))
    elif etapa == 'becerro':
        return hoy - timedelta(days=random.randint(30, 180))
    elif etapa == 'destete':
        return hoy - timedelta(days=random.randint(180, 365))
    elif etapa == 'engorde':
        return hoy - timedelta(days=random.randint(365, 730))
    elif etapa == 'toro':
        return hoy - timedelta(days=random.randint(1095, 3650))
    return hoy - timedelta(days=random.randint(365, 1095))

categorias_etapas = [
    ('preñada', 'Vaca preñada', 'H', 450, 650),
    ('lactante', 'Vaca lactante con cría', 'H', 400, 600),
    ('becerro', 'Becerro de cría', 'M', 100, 250),
    ('becerro', 'Becerra de cría', 'H', 90, 230),
    ('destete', 'Becerro destete', 'M', 250, 400),
    ('destete', 'Becerra destete', 'H', 230, 380),
    ('engorde', 'Novillo de engorde', 'M', 400, 550),
    ('toro', 'Toro reproductor', 'M', 700, 1000),
]

animales_creados = []
toros_reproductores = []
vacas_madres = []
aretes_usados = set()

def generar_arete_unico(prefix):
    while True:
        numero = random.randint(1000, 99999)
        arete = f"{prefix}{numero}"
        if arete not in aretes_usados:
            aretes_usados.add(arete)
            return arete

for finca in fincas_existentes:
    # Primero los reproductores
    for _ in range(10):
        tipo_animal = random.choice(['toro', 'preñada'])
        if tipo_animal == 'toro':
            etapa, nombre_categoria, sexo, peso_min, peso_max = ('toro', 'Toro reproductor', 'M', 700, 1000)
        else:
            etapa, nombre_categoria, sexo, peso_min, peso_max = ('preñada', 'Vaca preñada', 'H', 450, 650)
        
        arete = generar_arete_unico('A')
        animal = Animal.objects.create(
            numero_arete=arete,
            finca=finca,
            nombre_propio=f"{nombre_categoria} {finca.nombre[:3]}",
            fecha_nacimiento=generar_fecha_nacimiento(etapa),
            sexo=sexo,
            especie=especie_bovino,
            raza_declarada=random.choice(razas_creadas),
            categoria=nombre_categoria,
            estado='activo',
            is_active=True,
            observaciones=f"Animal de prueba para finca {finca.nombre}"
        )
        animales_creados.append(animal)
        if tipo_animal == 'toro':
            toros_reproductores.append(animal)
        else:
            vacas_madres.append(animal)
    
    # El resto de animales
    for _ in range(NUM_ANIMALES_POR_FINCA - 10):
        etapa, nombre_categoria, sexo, peso_min, peso_max = random.choice(categorias_etapas)
        
        padre = None
        madre = None
        if etapa in ['becerro', 'destete']:
            if toros_reproductores and vacas_madres:
                padre = random.choice(toros_reproductores)
                madre = random.choice(vacas_madres)
        
        arete = generar_arete_unico('B')
        animal = Animal.objects.create(
            numero_arete=arete,
            finca=finca,
            nombre_propio=f"{nombre_categoria} {random.randint(1, 100)}",
            fecha_nacimiento=generar_fecha_nacimiento(etapa),
            sexo=sexo,
            especie=especie_bovino,
            raza_declarada=random.choice(razas_creadas),
            categoria=nombre_categoria,
            padre=padre,
            madre=madre,
            estado='activo',
            is_active=True,
            observaciones=f"Animal de prueba para finca {finca.nombre}"
        )
        animales_creados.append(animal)
        if etapa == 'preñada':
            vacas_madres.append(animal)
        elif etapa == 'toro':
            toros_reproductores.append(animal)

print(f"✅ Creados {len(animales_creados)} animales en {len(fincas_existentes)} fincas. Aretes únicos garantizados.")

# ============================================================
# 5. ASIGNAR MOVIMIENTOS
# ============================================================
for animal in animales_creados:
    potrero = random.choice(potreros_totales)
    fecha_entrada = timezone.now()
    
    MovimientoAnimal.objects.create(
        animal=animal,
        finca=animal.finca,
        potrero=potrero,
        fecha_entrada=fecha_entrada,
        activo=True,
        tipo_pasto=random.choice(pastos_creados),
        observaciones=f"Movimiento de prueba"
    )
    potrero.carga_actual = MovimientoAnimal.objects.filter(potrero=potrero, activo=True).count()
    potrero.save()

print(f"✅ Movimientos asignados a todos los animales de las nuevas fincas.")

# ============================================================
# 6. GENERAR HISTORIAL DE SALUD
# ============================================================
eventos_salud = [
    ('vacunacion', 'Fiebre Aftosa', 'Vacuna trivalente'),
    ('vacunacion', 'Rabia', 'Vacuna antirrábica'),
    ('desparasitacion', 'Ivermectina', 'Desparasitante inyectable'),
    ('desparasitacion', 'Albendazol', 'Desparasitante oral'),
    ('enfermedad', 'Neumonía', 'Tratamiento con antibióticos'),
]

for animal in random.sample(animales_creados, min(100, len(animales_creados))):
    num_eventos = random.randint(2, 4)
    for _ in range(num_eventos):
        tipo, producto, descripcion = random.choice(eventos_salud)
        fecha_evento = timezone.now() - timedelta(days=random.randint(30, 365))
        
        EventoSalud.objects.create(
            animal=animal,
            finca=animal.finca,
            tipo=tipo,
            fecha=fecha_evento,
            producto=producto,
            dosis=random.choice(['5 ml', '10 ml', '1 dosis', '2 dosis']),
            nombre_veterinario=random.choice(['Dr. Pérez', 'Dra. Gómez', 'Dr. Rodríguez']),
            observaciones=descripcion
        )

print(f"✅ Historial de salud generado para 100 animales.")

# ============================================================
# 7. CREAR ADQUISICIONES Y VINCULAR ANIMALES
# ============================================================
print("\n⏳ Creando adquisiciones...")

for finca in fincas_existentes:
    # Crear una adquisición para esta finca
    adq = Adquisicion.objects.create(
        finca=finca,
        proveedor=f"Proveedor {finca.nombre}",
        fecha=FECHA_ACTUAL,
        numero_documento=f"FAC-{finca.id}-{random.randint(1000, 9999)}",
        costo_total=Decimal(random.uniform(5000, 50000)),
        observaciones=f"Adquisición de prueba para {finca.nombre}"
    )
    
    # Elegir 10 animales al azar de esta finca y vincularlos a la adquisición
    animales_finca = [a for a in animales_creados if a.finca_id == finca.id]
    for animal in random.sample(animales_finca, min(10, len(animales_finca))):
        AdquisicionAnimal.objects.create(
            adquisicion=adq,
            animal=animal,
            precio_individual=Decimal(random.uniform(1000, 5000)),
            observaciones=f"Animal incluido en {adq.numero_documento}"
        )

print(f"✅ Adquisiciones creadas y vinculadas a animales.")

# ============================================================
# 8. GENERAR PESAJE MENSUAL
# ============================================================
pesos_por_etapa = {
    'preñada': (450, 650),
    'lactante': (400, 600),
    'becerro': (100, 250),
    'destete': (250, 400),
    'engorde': (400, 550),
    'toro': (700, 1000),
}

for animal in animales_creados:
    if random.random() < 0.6:
        peso_min, peso_max = pesos_por_etapa.get(animal.categoria, (300, 500))
        for i in range(6):
            fecha_pesaje = timezone.now() - timedelta(days=30 * i)
            peso = Decimal(random.uniform(peso_min, peso_max))
            
            PesajeAnimal.objects.create(
                animal=animal,
                finca=animal.finca,
                fecha=fecha_pesaje,
                peso_kg=peso,
                observaciones=f"Pesaje de control mensual (mes {i+1})"
            )

print(f"✅ Pesajes mensuales generados para 300 animales.")

print("\n🎉 ¡CARGA MASIVA MULTI-FINCA COMPLETADA!")
print(f"📊 Resumen:")
print(f"  - {len(fincas_existentes)} fincas utilizadas")
print(f"  - {len(potreros_totales)} potreros creados")
print(f"  - {len(animales_creados)} nuevos animales (con aretes únicos)")
print(f"  - Adquisiciones y vinculaciones creadas.")
print(f"  - La finca original 'Hato La Coromoto' quedó intacta.")
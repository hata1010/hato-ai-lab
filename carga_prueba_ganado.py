import os
from datetime import timedelta
from decimal import Decimal

from django.contrib.gis.geos import Polygon
from django.utils import timezone


# ============================================================
# CONFIGURACIÓN DJANGO
# ============================================================

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()


# ============================================================
# MODELOS
# ============================================================

from apps.core.models import Finca, Potrero

from apps.ganado.models import (
    Especie,
    Raza,
    TipoPasto,
    Animal,
    MovimientoAnimal,
    EventoSalud,
    PesajeAnimal,
    Adquisicion,
    AdquisicionAnimal,
)


# ============================================================
# CONFIGURACIÓN DE LA PRUEBA
# ============================================================

NOMBRE_FINCA = "Hato Prueba Ganado"

NIT_FINCA = "J-99999999-9"

NUM_POTREROS = 3

FECHA_HOY = timezone.now().date()


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def crear_poligono(lat, lon, tamaño=0.003):
    """
    Crea un cuadrado sencillo alrededor de una coordenada.
    """

    return Polygon(
        (
            (lon - tamaño, lat - tamaño),
            (lon + tamaño, lat - tamaño),
            (lon + tamaño, lat + tamaño),
            (lon - tamaño, lat + tamaño),
            (lon - tamaño, lat - tamaño),
        ),
        srid=4326,
    )


def crear_animal(**datos):
    """
    Crea un animal ejecutando también full_clean()
    para que las validaciones del modelo se ejecuten.
    """

    animal = Animal(**datos)

    animal.full_clean()

    animal.save()

    return animal


def crear_movimiento(**datos):
    """
    Crea un movimiento validando primero el modelo.
    """

    movimiento = MovimientoAnimal(**datos)

    movimiento.full_clean()

    movimiento.save()

    return movimiento


# ============================================================
# 1. ESPECIE
# ============================================================

especie, _ = Especie.objects.get_or_create(
    nombre="Bovino",
    defaults={
        "descripcion": (
            "Ganado vacuno utilizado para producción "
            "de carne, leche y reproducción."
        )
    },
)

print(f"✓ Especie: {especie}")


# ============================================================
# 2. RAZAS
# ============================================================

razas = []

for nombre in [
    "Brahman",
    "Criollo",
    "Pardo Suizo",
]:

    raza, _ = Raza.objects.get_or_create(
        nombre=nombre,
        especie=especie,
        defaults={
            "descripcion": f"Raza bovina {nombre}."
        },
    )

    razas.append(raza)

print(f"✓ Razas disponibles: {len(razas)}")


# ============================================================
# 3. TIPOS DE PASTO
# ============================================================

pastos = []

for nombre in [
    "Brachiaria",
    "Guinea",
    "Estrella",
]:

    pasto, _ = TipoPasto.objects.get_or_create(
        nombre=nombre,
        defaults={
            "descripcion": f"Pasto de prueba {nombre}."
        },
    )

    pastos.append(pasto)

print(f"✓ Tipos de pasto disponibles: {len(pastos)}")


# ============================================================
# 4. CREAR FINCA DE PRUEBA
# ============================================================

finca, creada = Finca.objects.get_or_create(
    nombre=NOMBRE_FINCA,
    defaults={
        "nit": NIT_FINCA,
        "direccion": "Finca utilizada para pruebas del módulo ganado",
        "zona_horaria": "America/Caracas",
        "moneda": "VES",
        "area_total": Decimal("120.00"),
        "is_active": True,
        "descripcion": (
            "Finca creada exclusivamente para pruebas "
            "del modelo de ganado."
        ),
    },
)

if creada:
    print(f"✓ Finca creada: {finca.nombre}")
else:
    print(f"✓ Finca existente utilizada: {finca.nombre}")


# ============================================================
# 5. CREAR POTREROS
# ============================================================

potreros = []

potreros_data = [
    {
        "nombre": "Potrero Prueba 01",
        "codigo": "PRUEBA-01",
        "lat": 8.9000,
        "lon": -67.4000,
        "tipo": "potrero",
        "area": Decimal("10.00"),
        "capacidad": 20,
        "pasto": pastos[0],
    },
    {
        "nombre": "Potrero Prueba 02",
        "codigo": "PRUEBA-02",
        "lat": 8.9050,
        "lon": -67.3950,
        "tipo": "potrero",
        "area": Decimal("8.00"),
        "capacidad": 15,
        "pasto": pastos[1],
    },
    {
        "nombre": "Potrero Prueba 03",
        "codigo": "PRUEBA-03",
        "lat": 8.9100,
        "lon": -67.3900,
        "tipo": "potrero",
        "area": Decimal("12.00"),
        "capacidad": 25,
        "pasto": pastos[2],
    },
]


for data in potreros_data:

    potrero, creada = Potrero.objects.get_or_create(
        finca=finca,
        codigo=data["codigo"],
        defaults={
            "nombre": data["nombre"],
            "tipo": data["tipo"],
            "poligono": crear_poligono(
                data["lat"],
                data["lon"],
            ),
            "area_hectareas": data["area"],
            "capacidad_animales": data["capacidad"],
            "carga_actual": 0,
            "estado": "disponible",
            "tipo_pasto": data["pasto"],
            "is_active": True,
        },
    )

    potreros.append(potrero)

    print(
        f"✓ Potrero: {potrero.nombre} "
        f"→ {finca.nombre}"
    )


# ============================================================
# 6. CREAR ANIMALES
# ============================================================

animales = []

# ------------------------------------------------------------
# TOROS
# ------------------------------------------------------------

toros = []

for i in range(2):

    toro = crear_animal(
        numero_arete=f"PR-T-{i + 1:03d}",
        nombre_propio=f"Toro Prueba {i + 1}",
        fecha_nacimiento=FECHA_HOY - timedelta(
            days=1200 + (i * 180)
        ),
        sexo="M",
        especie=especie,
        raza_declarada=razas[0],
        categoria="Toro reproductor",
        finca=finca,
        estado="activo",
        is_active=True,
        observaciones=(
            "Animal creado para pruebas "
            "del módulo ganado."
        ),
    )

    toros.append(toro)
    animales.append(toro)

    print(f"✓ Toro creado: {toro}")


# ------------------------------------------------------------
# VACAS
# ------------------------------------------------------------

vacas = []

for i in range(6):

    vaca = crear_animal(
        numero_arete=f"PR-V-{i + 1:03d}",
        nombre_propio=f"Vaca Prueba {i + 1}",
        fecha_nacimiento=FECHA_HOY - timedelta(
            days=1000 + (i * 90)
        ),
        sexo="H",
        especie=especie,
        raza_declarada=razas[i % len(razas)],
        categoria="Vaca reproductora",
        finca=finca,
        estado="activo",
        is_active=True,
        observaciones=(
            "Animal creado para pruebas "
            "del módulo ganado."
        ),
    )

    vacas.append(vaca)
    animales.append(vaca)

    print(f"✓ Vaca creada: {vaca}")


# ------------------------------------------------------------
# ANIMALES JÓVENES
# ------------------------------------------------------------

for i in range(4):

    sexo = "M" if i < 2 else "H"

    padre = toros[i % len(toros)]
    madre = vacas[i % len(vacas)]

    joven = crear_animal(
        numero_arete=f"PR-J-{i + 1:03d}",
        nombre_propio=f"Joven Prueba {i + 1}",
        fecha_nacimiento=FECHA_HOY - timedelta(
            days=180 + (i * 30)
        ),
        sexo=sexo,
        especie=especie,
        raza_declarada=razas[i % len(razas)],
        categoria="Becerro" if sexo == "M" else "Becerra",
        finca=finca,
        padre=padre,
        madre=madre,
        estado="activo",
        is_active=True,
        observaciones=(
            "Animal joven creado para pruebas "
            "de genealogía."
        ),
    )

    animales.append(joven)

    print(
        f"✓ Animal joven creado: {joven} "
        f"(padre={padre}, madre={madre})"
    )


print()
print(f"✓ TOTAL ANIMALES CREADOS: {len(animales)}")


# ============================================================
# 7. DISTRIBUIR LOS ANIMALES EN POTREROS
# ============================================================

# Potrero 01 → 5 animales
# Potrero 02 → 7 animales
# Potrero 03 → 0 animales

asignaciones = [
    potreros[0],
    potreros[0],
    potreros[0],
    potreros[0],
    potreros[0],

    potreros[1],
    potreros[1],
    potreros[1],
    potreros[1],
    potreros[1],
    potreros[1],
    potreros[1],
]


for animal, potrero in zip(animales, asignaciones):

    movimiento = crear_movimiento(
        animal=animal,
        potrero=potrero,
        fecha_entrada=timezone.now(),
        fecha_salida=None,
        activo=True,
        tipo_pasto=potrero.tipo_pasto,
        observaciones="Ubicación inicial de prueba.",
    )

    print(
        f"✓ {animal} → {potrero.nombre}"
    )


# ============================================================
# 8. ACTUALIZAR CARGA DE LOS POTREROS
# ============================================================

for potrero in potreros:

    carga = MovimientoAnimal.objects.filter(
        potrero=potrero,
        activo=True,
    ).count()

    potrero.carga_actual = carga

    # Estado lógico para la prueba
    if carga == 0:
        potrero.estado = "disponible"
    else:
        potrero.estado = "ocupado"

    potrero.save(
        update_fields=[
            "carga_actual",
            "estado",
        ]
    )

    print(
        f"✓ {potrero.nombre}: "
        f"{carga} animales"
    )


# ============================================================
# 9. EVENTOS DE SALUD
# ============================================================

eventos = [
    (
        "vacunacion",
        "Fiebre Aftosa",
        "Vacunación preventiva",
    ),
    (
        "desparasitacion",
        "Ivermectina",
        "Desparasitación preventiva",
    ),
    (
        "examen",
        "Revisión general",
        "Control veterinario",
    ),
]


for i, animal in enumerate(animales):

    tipo, producto, observacion = eventos[
        i % len(eventos)
    ]

    EventoSalud.objects.create(
        animal=animal,
        tipo=tipo,
        fecha=timezone.now() - timedelta(
            days=30 + i
        ),
        producto=producto,
        dosis="1 dosis",
        nombre_veterinario="Veterinario de prueba",
        observaciones=observacion,
    )


print(
    f"✓ Eventos de salud creados: {len(animales)}"
)


# ============================================================
# 10. PESAJE
# ============================================================

pesos_base = {
    "Toro reproductor": 800,
    "Vaca reproductora": 500,
    "Becerro": 220,
    "Becerra": 200,
}


for i, animal in enumerate(animales):

    peso_base = pesos_base.get(
        animal.categoria,
        300,
    )

    for mes in range(3):

        peso = Decimal(
            peso_base + (mes * 10)
        )

        PesajeAnimal.objects.create(
            animal=animal,
            fecha=timezone.now()
            - timedelta(days=30 * mes),
            peso_kg=peso,
            observaciones=(
                f"Pesaje de prueba "
                f"mes {mes + 1}"
            ),
        )


print(
    f"✓ Pesajes creados: "
    f"{len(animales) * 3}"
)


# ============================================================
# 11. ADQUISICIÓN
# ============================================================

adquisicion = Adquisicion.objects.create(
    finca=finca,
    proveedor="Proveedor de Prueba",
    fecha=FECHA_HOY,
    numero_documento="PRUEBA-0001",
    costo_total=Decimal("24000.00"),
    observaciones=(
        "Adquisición creada exclusivamente "
        "para pruebas."
    ),
)

print(
    f"✓ Adquisición creada: "
    f"{adquisicion.numero_documento}"
)


# ------------------------------------------------------------
# Vincular 4 animales
# ------------------------------------------------------------

for i, animal in enumerate(animales[:4]):

    AdquisicionAnimal.objects.create(
        adquisicion=adquisicion,
        animal=animal,
        precio_individual=Decimal(
            "6000.00"
        ),
        observaciones=(
            "Animal incluido en adquisición "
            "de prueba."
        ),
    )


print(
    "✓ 4 animales vinculados a la adquisición"
)


# ============================================================
# 12. RESUMEN FINAL
# ============================================================

print()
print("=" * 60)
print("      CARGA DE PRUEBA COMPLETADA")
print("=" * 60)

print(f"Finca:              {finca.nombre}")
print(f"Potreros:           {len(potreros)}")
print(f"Animales:           {len(animales)}")
print(
    f"Movimientos activos: "
    f"{MovimientoAnimal.objects.filter(
        animal__finca=finca,
        activo=True
    ).count()}"
)

print(
    f"Eventos de salud: "
    f"{EventoSalud.objects.filter(
        animal__finca=finca
    ).count()}"
)

print(
    f"Pesajes: "
    f"{PesajeAnimal.objects.filter(
        animal__finca=finca
    ).count()}"
)

print(
    f"Adquisiciones: "
    f"{Adquisicion.objects.filter(
        finca=finca
    ).count()}"
)

print()
print("DISTRIBUCIÓN DE POTREROS:")

for potrero in potreros:

    print(
        f"  {potrero.nombre}: "
        f"{potrero.carga_actual} animales"
    )

print()
print("✓ La finca original NO fue modificada.")
print("✓ La carga pertenece a una finca independiente.")
print("✓ Los animales pertenecen a la finca.")
print("✓ La ubicación se determina mediante MovimientoAnimal.")
print("✓ Un potrero puede estar vacío.")
print("=" * 60)
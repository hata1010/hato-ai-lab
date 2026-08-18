import os
from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.contrib.gis.geos import Polygon
from django.utils import timezone


# ============================================================
# CONFIGURACIÓN DJANGO
# ============================================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

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
# CONFIGURACIÓN
# ============================================================

FECHA_HOY = timezone.now().date()


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def crear_poligono(lat, lon, tamaño=0.003):
    """
    Crea un cuadrado sencillo alrededor
    de una coordenada.
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
    Crea un animal ejecutando full_clean()
    antes de guardarlo.
    """

    animal = Animal(**datos)

    animal.full_clean()
    animal.save()

    return animal


def crear_movimiento(**datos):
    """
    Crea un movimiento validando primero
    el modelo.
    """

    movimiento = MovimientoAnimal(**datos)

    movimiento.full_clean()
    movimiento.save()

    return movimiento


# ============================================================
# 1. OBTENER TABLAS MAESTRAS EXISTENTES
# ============================================================

print()
print("=" * 70)
print("   VERIFICANDO TABLAS MAESTRAS")
print("=" * 70)

especie = Especie.objects.filter(
    nombre="Bovino"
).first()

if not especie:
    raise RuntimeError(
        "No existe la especie 'Bovino'. "
        "Ejecuta primero la carga de prueba original."
    )

print(f"✓ Especie utilizada: {especie}")


# ------------------------------------------------------------
# RAZAS
# ------------------------------------------------------------

razas = []

for nombre in [
    "Brahman",
    "Criollo",
    "Pardo Suizo",
]:

    raza = Raza.objects.filter(
        nombre=nombre,
        especie=especie,
    ).first()

    if not raza:
        raise RuntimeError(
            f"No existe la raza '{nombre}'. "
            "Ejecuta primero la carga de prueba original."
        )

    razas.append(raza)

print(f"✓ Razas utilizadas: {len(razas)}")


# ------------------------------------------------------------
# PASTOS
# ------------------------------------------------------------

pastos = []

for nombre in [
    "Brachiaria",
    "Guinea",
    "Estrella",
]:

    pasto = TipoPasto.objects.filter(
        nombre=nombre
    ).first()

    if not pasto:
        raise RuntimeError(
            f"No existe el tipo de pasto '{nombre}'. "
            "Ejecuta primero la carga de prueba original."
        )

    pastos.append(pasto)

print(f"✓ Tipos de pasto utilizados: {len(pastos)}")


# ============================================================
# FUNCIÓN PRINCIPAL PARA CREAR UNA FINCA DE PRUEBA
# ============================================================

def crear_finca_prueba(
    nombre_finca,
    nit_finca,
    prefijo,
    area_total,
    potreros_data,
    numero_documento,
):
    """
    Crea una finca independiente con:

        - 3 potreros
        - 2 toros
        - 6 vacas
        - 4 animales jóvenes
        - movimientos
        - eventos de salud
        - pesajes
        - adquisición

    Las tablas maestras son compartidas.
    """

    print()
    print("=" * 70)
    print(f"CREANDO: {nombre_finca}")
    print("=" * 70)

    # --------------------------------------------------------
    # SEGURIDAD: NO DUPLICAR FINCA
    # --------------------------------------------------------

    if Finca.objects.filter(
        nombre=nombre_finca
    ).exists():

        raise RuntimeError(
            f"La finca '{nombre_finca}' ya existe. "
            "El script se detiene para evitar duplicaciones."
        )

    if Finca.objects.filter(
        nit=nit_finca
    ).exists():

        raise RuntimeError(
            f"El NIT '{nit_finca}' ya existe. "
            "El script se detiene para evitar conflictos."
        )

    # --------------------------------------------------------
    # TODO LO DE ESTA FINCA ES UNA TRANSACCIÓN
    # --------------------------------------------------------

    with transaction.atomic():

        # ====================================================
        # FINCA
        # ====================================================

        finca = Finca.objects.create(
            nombre=nombre_finca,
            nit=nit_finca,
            direccion=(
                f"Finca utilizada para pruebas "
                f"de multifinca - {nombre_finca}"
            ),
            zona_horaria="America/Caracas",
            moneda="VES",
            area_total=Decimal(str(area_total)),
            is_active=True,
            descripcion=(
                "Finca creada exclusivamente para "
                "pruebas del modelo multifinca."
            ),
        )

        print(
            f"✓ Finca creada: {finca.nombre}"
        )

        # ====================================================
        # POTREROS
        # ====================================================

        potreros = []

        for data in potreros_data:

            potrero = Potrero.objects.create(
                finca=finca,
                nombre=data["nombre"],
                codigo=data["codigo"],
                tipo="potrero",
                poligono=crear_poligono(
                    data["lat"],
                    data["lon"],
                    data.get("tamaño", 0.003),
                ),
                area_hectareas=Decimal(
                    str(data["area"])
                ),
                capacidad_animales=data["capacidad"],
                carga_actual=0,
                estado="disponible",
                tipo_pasto=data["pasto"],
                is_active=True,
            )

            potreros.append(potrero)

            print(
                f"✓ Potrero creado: "
                f"{potrero.nombre} → {finca.nombre}"
            )

        # ====================================================
        # ANIMALES
        # ====================================================

        animales = []

        # ----------------------------------------------------
        # TOROS
        # ----------------------------------------------------

        toros = []

        for i in range(2):

            toro = crear_animal(
                numero_arete=f"{prefijo}-T-{i + 1:03d}",
                nombre_propio=(
                    f"{nombre_finca} - Toro {i + 1}"
                ),
                fecha_nacimiento=(
                    FECHA_HOY
                    - timedelta(
                        days=1200 + (i * 180)
                    )
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
                    "multifinca."
                ),
            )

            toros.append(toro)
            animales.append(toro)

            print(
                f"✓ Toro: {toro.numero_arete}"
            )

        # ----------------------------------------------------
        # VACAS
        # ----------------------------------------------------

        vacas = []

        for i in range(6):

            vaca = crear_animal(
                numero_arete=f"{prefijo}-V-{i + 1:03d}",
                nombre_propio=(
                    f"{nombre_finca} - Vaca {i + 1}"
                ),
                fecha_nacimiento=(
                    FECHA_HOY
                    - timedelta(
                        days=1000 + (i * 90)
                    )
                ),
                sexo="H",
                especie=especie,
                raza_declarada=(
                    razas[i % len(razas)]
                ),
                categoria="Vaca reproductora",
                finca=finca,
                estado="activo",
                is_active=True,
                observaciones=(
                    "Animal creado para pruebas "
                    "multifinca."
                ),
            )

            vacas.append(vaca)
            animales.append(vaca)

            print(
                f"✓ Vaca: {vaca.numero_arete}"
            )

        # ----------------------------------------------------
        # ANIMALES JÓVENES
        # ----------------------------------------------------

        for i in range(4):

            sexo = "M" if i < 2 else "H"

            padre = toros[
                i % len(toros)
            ]

            madre = vacas[
                i % len(vacas)
            ]

            joven = crear_animal(
                numero_arete=(
                    f"{prefijo}-J-{i + 1:03d}"
                ),
                nombre_propio=(
                    f"{nombre_finca} - Joven {i + 1}"
                ),
                fecha_nacimiento=(
                    FECHA_HOY
                    - timedelta(
                        days=180 + (i * 30)
                    )
                ),
                sexo=sexo,
                especie=especie,
                raza_declarada=(
                    razas[i % len(razas)]
                ),
                categoria=(
                    "Becerro"
                    if sexo == "M"
                    else "Becerra"
                ),
                finca=finca,
                padre=padre,
                madre=madre,
                estado="activo",
                is_active=True,
                observaciones=(
                    "Animal joven creado para "
                    "pruebas de genealogía."
                ),
            )

            animales.append(joven)

            print(
                f"✓ Joven: "
                f"{joven.numero_arete}"
            )

        print(
            f"✓ TOTAL ANIMALES: "
            f"{len(animales)}"
        )

        # ====================================================
        # MOVIMIENTOS
        # ====================================================

        # 5 animales → Potrero 1
        # 7 animales → Potrero 2
        # 0 animales → Potrero 3

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

        for animal, potrero in zip(
            animales,
            asignaciones,
        ):

            crear_movimiento(
                animal=animal,
                potrero=potrero,
                fecha_entrada=timezone.now(),
                fecha_salida=None,
                activo=True,
                tipo_pasto=potrero.tipo_pasto,
                observaciones=(
                    "Ubicación inicial "
                    "de prueba multifinca."
                ),
            )

            print(
                f"✓ {animal.numero_arete} "
                f"→ {potrero.nombre}"
            )

        # ====================================================
        # CARGA DE POTREROS
        # ====================================================

        for potrero in potreros:

            carga = MovimientoAnimal.objects.filter(
                potrero=potrero,
                activo=True,
            ).count()

            potrero.carga_actual = carga

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

        # ====================================================
        # EVENTOS DE SALUD
        # ====================================================

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
                fecha=(
                    timezone.now()
                    - timedelta(days=30 + i)
                ),
                producto=producto,
                dosis="1 dosis",
                nombre_veterinario=(
                    "Veterinario de prueba"
                ),
                observaciones=observacion,
            )

        print(
            f"✓ Eventos de salud: "
            f"{len(animales)}"
        )

        # ====================================================
        # PESAJES
        # ====================================================

        pesos_base = {
            "Toro reproductor": 800,
            "Vaca reproductora": 500,
            "Becerro": 220,
            "Becerra": 200,
        }

        for animal in animales:

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
                    fecha=(
                        timezone.now()
                        - timedelta(
                            days=30 * mes
                        )
                    ),
                    peso_kg=peso,
                    observaciones=(
                        f"Pesaje de prueba "
                        f"mes {mes + 1}"
                    ),
                )

        print(
            f"✓ Pesajes: "
            f"{len(animales) * 3}"
        )

        # ====================================================
        # ADQUISICIÓN
        # ====================================================

        adquisicion = Adquisicion.objects.create(
            finca=finca,
            proveedor=(
                f"Proveedor de Prueba "
                f"{prefijo}"
            ),
            fecha=FECHA_HOY,
            numero_documento=numero_documento,
            costo_total=Decimal(
                "24000.00"
            ),
            observaciones=(
                "Adquisición creada "
                "para pruebas multifinca."
            ),
        )

        print(
            f"✓ Adquisición: "
            f"{adquisicion.numero_documento}"
        )

        # ----------------------------------------------------
        # VINCULAR 4 ANIMALES
        # ----------------------------------------------------

        for animal in animales[:4]:

            AdquisicionAnimal.objects.create(
                adquisicion=adquisicion,
                animal=animal,
                precio_individual=Decimal(
                    "6000.00"
                ),
                observaciones=(
                    "Animal incluido en "
                    "adquisición de prueba."
                ),
            )

        print(
            "✓ 4 animales vinculados "
            "a la adquisición"
        )

        # ====================================================
        # RESUMEN
        # ====================================================

    print()
    print(
        f"✓ FINCA COMPLETADA: {finca.nombre}"
    )

    print(
        f"  Potreros: {len(potreros)}"
    )

    print(
        f"  Animales: {len(animales)}"
    )

    movimientos_activos = MovimientoAnimal.objects.filter(
        animal__finca=finca,
        activo=True,
    ).count()

    eventos_salud = EventoSalud.objects.filter(
        animal__finca=finca,
    ).count()

    pesajes = PesajeAnimal.objects.filter(
        animal__finca=finca,
    ).count()

    adquisiciones = Adquisicion.objects.filter(
        finca=finca,
    ).count()

    print(
        f"  Movimientos activos: {movimientos_activos}"
    )

    print(
        f"  Eventos salud: {eventos_salud}"
    )

    print(
        f"  Pesajes: {pesajes}"
    )

    print(
        f"  Adquisiciones: {adquisiciones}"
    )

    return finca

    return finca


# ============================================================
# FINCA 2
# ============================================================

finca_2 = crear_finca_prueba(

    nombre_finca="Hato Prueba Oriente",

    nit_finca="J-88888888-8",

    prefijo="OR",

    area_total="150.00",

    potreros_data=[
        {
            "nombre": "Oriente Potrero 01",
            "codigo": "OR-PR-01",
            "lat": 9.0500,
            "lon": -67.3000,
            "area": "12.00",
            "capacidad": 25,
            "pasto": pastos[0],
        },
        {
            "nombre": "Oriente Potrero 02",
            "codigo": "OR-PR-02",
            "lat": 9.0550,
            "lon": -67.2950,
            "area": "10.00",
            "capacidad": 20,
            "pasto": pastos[1],
        },
        {
            "nombre": "Oriente Potrero 03",
            "codigo": "OR-PR-03",
            "lat": 9.0600,
            "lon": -67.2900,
            "area": "15.00",
            "capacidad": 30,
            "pasto": pastos[2],
        },
    ],

    numero_documento="OR-ADQ-0001",
)


# ============================================================
# FINCA 3
# ============================================================

finca_3 = crear_finca_prueba(

    nombre_finca="Hato Prueba Llanero",

    nit_finca="J-77777777-7",

    prefijo="LL",

    area_total="200.00",

    potreros_data=[
        {
            "nombre": "Llanero Potrero 01",
            "codigo": "LL-PR-01",
            "lat": 8.7500,
            "lon": -67.5500,
            "area": "20.00",
            "capacidad": 35,
            "pasto": pastos[0],
        },
        {
            "nombre": "Llanero Potrero 02",
            "codigo": "LL-PR-02",
            "lat": 8.7550,
            "lon": -67.5450,
            "area": "18.00",
            "capacidad": 30,
            "pasto": pastos[1],
        },
        {
            "nombre": "Llanero Potrero 03",
            "codigo": "LL-PR-03",
            "lat": 8.7600,
            "lon": -67.5400,
            "area": "22.00",
            "capacidad": 40,
            "pasto": pastos[2],
        },
    ],

    numero_documento="LL-ADQ-0001",
)


# ============================================================
# RESUMEN GENERAL
# ============================================================

print()
print()
print("=" * 70)
print("       CARGA DE DOS FINCAS COMPLETADA")
print("=" * 70)

print()
print("FINCAS CREADAS:")

print(
    f"  1. {finca_2.nombre}"
)

print(
    f"  2. {finca_3.nombre}"
)

print()
print("✓ Las tablas maestras fueron reutilizadas.")
print("✓ Cada finca tiene sus propios potreros.")
print("✓ Cada finca tiene sus propios animales.")
print("✓ Cada finca tiene sus propios movimientos.")
print("✓ Cada finca tiene sus propios eventos de salud.")
print("✓ Cada finca tiene sus propios pesajes.")
print("✓ Cada finca tiene su propia adquisición.")
print("✓ Los aretes de los animales son diferentes.")
print("✓ Los códigos de potreros son diferentes.")
print("✓ Los documentos de adquisición son diferentes.")
print()
print("IMPORTANTE:")
print("La finca original NO fue modificada.")
print("=" * 70)
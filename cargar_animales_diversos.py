"""
Carga de animales de prueba DIVERSOS por finca.

OBJETIVO
--------
Crear una huella de datos claramente diferente en cada finca existente,
para validar el aislamiento multi-finca del Dashboard Operativo V2.

REGLAS
------
- NO crea fincas.
- NO elimina ni modifica animales existentes.
- Solo agrega animales nuevos y sus pesajes.
- Cada finca recibe una cantidad y distribucion diferente.
- Los valores se generan de forma reproducible mediante una semilla
  distinta por finca.
- El script es idempotente respecto de sus propios registros: si ya
  encuentra el arete generado, no lo duplica.
- Usa full_clean() antes de guardar Animal, igual que los cargadores
  existentes del proyecto.
- Cada finca se procesa dentro de una transaccion atomica.

EJECUCION EN KATIA3
-------------------
    python cargar_animales_diversos.py

NOTA
----
Este archivo esta pensado para el entorno de pruebas/desarrollo.
No debe ejecutarse contra una base de datos de produccion sin revisar
previamente el dataset objetivo.
"""

import os
import random
from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from apps.core.models import Finca
from apps.ganado.models import Animal, Especie, Raza, PesajeAnimal


FECHA_HOY = timezone.now().date()

# Cada finca tiene una firma deliberadamente diferente.
# (categoria, sexo, cantidad, edad_min_dias, edad_max_dias,
#  peso_min_kg, peso_max_kg)
PERFILES = {
    "Hato Prueba Oriente": {
        "seed": 210821,
        "prefijo": "OR-D",
        "firma": [
            ("Vaca reproductora", "H", 9, 900, 2600, 410, 620),
            ("Toro reproductor", "M", 2, 1500, 3000, 650, 920),
            ("Becerro", "M", 4, 120, 480, 120, 285),
            ("Becerra", "H", 2, 150, 520, 110, 270),
        ],
    },
    "Hato Prueba Llanero": {
        "seed": 210822,
        "prefijo": "LL-D",
        "firma": [
            ("Vaca reproductora", "H", 3, 1100, 2100, 480, 690),
            ("Toro reproductor", "M", 1, 1800, 3300, 760, 980),
            ("Becerro", "M", 1, 80, 260, 85, 175),
            ("Becerra", "H", 4, 70, 330, 75, 205),
        ],
    },
    "Hato Prueba Ganado": {
        "seed": 210823,
        "prefijo": "PR-D",
        "firma": [
            ("Vaca reproductora", "H", 8, 700, 3400, 360, 760),
            ("Toro reproductor", "M", 4, 1200, 3600, 620, 1050),
            ("Becerro", "M", 8, 90, 600, 95, 330),
            ("Becerra", "H", 3, 90, 650, 90, 315),
        ],
    },
}


def obtener_maestros():
    especie = Especie.objects.filter(nombre="Bovino").first()
    if not especie:
        raise RuntimeError(
            "No existe la especie 'Bovino'. Ejecuta primero los cargadores "
            "de datos de prueba existentes."
        )

    razas = list(Raza.objects.filter(especie=especie).order_by("id"))
    if not razas:
        raise RuntimeError(
            "No existen razas para Bovino. Ejecuta primero los cargadores "
            "de datos de prueba existentes."
        )

    return especie, razas


def siguiente_arete(finca, prefijo, usados):
    """Devuelve un arete nuevo sin tocar registros existentes."""
    numero = 1
    while True:
        arete = f"{prefijo}-{numero:03d}"
        if arete not in usados and not Animal.objects.filter(
            finca=finca, numero_arete=arete
        ).exists():
            usados.add(arete)
            return arete
        numero += 1


def crear_animal(finca, especie, razas, rng, prefijo, usado, especificacion):
    categoria, sexo, _cantidad, edad_min, edad_max, peso_min, peso_max = especificacion

    edad_dias = rng.randint(edad_min, edad_max)
    fecha_nacimiento = FECHA_HOY - timedelta(days=edad_dias)
    raza = rng.choice(razas)
    arete = siguiente_arete(finca, prefijo, usado)

    animal = Animal(
        numero_arete=arete,
        nombre_propio=f"Dato diverso {arete}",
        fecha_nacimiento=fecha_nacimiento,
        sexo=sexo,
        especie=especie,
        raza_declarada=raza,
        categoria=categoria,
        finca=finca,
        estado="activo",
        is_active=True,
        observaciones=(
            "Animal adicional generado para pruebas diferenciales del "
            "Dashboard Operativo V2. Dataset reproducible."
        ),
    )

    animal.full_clean()
    animal.save()

    # Dos pesajes separados para que el Dashboard no conserve el mismo
    # promedio ni la misma lista de ultimos pesajes entre fincas.
    peso_1 = Decimal(str(rng.randint(peso_min, peso_max)))
    variacion = Decimal(str(rng.randint(3, max(4, min(35, (peso_max - peso_min) // 4 or 4)))))
    peso_2 = max(Decimal("1"), peso_1 + variacion)

    PesajeAnimal.objects.create(
        animal=animal,
        fecha=timezone.now() - timedelta(days=rng.randint(10, 60)),
        peso_kg=peso_1,
        observaciones="Pesaje inicial del dataset diferencial.",
    )
    PesajeAnimal.objects.create(
        animal=animal,
        fecha=timezone.now() - timedelta(days=rng.randint(0, 9)),
        peso_kg=peso_2,
        observaciones="Pesaje reciente del dataset diferencial.",
    )

    return animal


def cargar_finca(finca, perfil, especie, razas):
    rng = random.Random(perfil["seed"])
    creados = []
    usados = set()

    with transaction.atomic():
        for especificacion in perfil["firma"]:
            cantidad = especificacion[2]
            for _ in range(cantidad):
                creados.append(
                    crear_animal(
                        finca=finca,
                        especie=especie,
                        razas=razas,
                        rng=rng,
                        prefijo=perfil["prefijo"],
                        usado=usados,
                        especificacion=especificacion,
                    )
                )

    return creados


def main():
    print("=" * 78)
    print(" HATO AI LAB · DATASET DIFERENCIAL PARA DASHBOARD OPERATIVO V2")
    print("=" * 78)

    especie, razas = obtener_maestros()
    total_creados = 0

    for nombre_finca, perfil in PERFILES.items():
        finca = Finca.objects.filter(nombre=nombre_finca, is_active=True).first()
        if not finca:
            raise RuntimeError(
                f"No se encontro la finca activa requerida: '{nombre_finca}'."
            )

        existentes_antes = Animal.objects.filter(
            finca=finca, estado="activo", is_active=True
        ).count()

        creados = cargar_finca(finca, perfil, especie, razas)
        existentes_despues = Animal.objects.filter(
            finca=finca, estado="activo", is_active=True
        ).count()

        print()
        print(f"FINCA: {finca.nombre}")
        print(f"  Antes:     {existentes_antes} animales activos")
        print(f"  Agregados: {len(creados)} animales")
        print(f"  Ahora:     {existentes_despues} animales activos")
        print(
            "  Firma:     "
            + ", ".join(
                f"{categoria}={cantidad}"
                for categoria, _sexo, cantidad, *_resto in perfil["firma"]
            )
        )

        total_creados += len(creados)

    print()
    print("=" * 78)
    print(f"TOTAL ANIMALES NUEVOS: {total_creados}")
    print("Las tres fincas conservan sus datos anteriores.")
    print("Cada finca recibio una firma estadistica diferente.")
    print("=" * 78)


if __name__ == "__main__":
    main()

from django.db import transaction

from .models import (
    Adquisicion,
    AdquisicionAnimal,
    Animal,
    MovimientoAnimal,
    PesajeAnimal,
    ProcedenciaAnimal,
)
from .models_reproduccion import CriaNacimiento, EventoReproductivo


@transaction.atomic
def registrar_ingreso_compra(*, finca, animal, proveedor, fecha_compra, documento_compra="", precio_individual=None, peso_inicial=None, potrero_inicial=None, observaciones=""):
    animal.finca = finca
    animal.save()

    ProcedenciaAnimal.objects.update_or_create(
        animal=animal,
        defaults={
            "tipo": "compra",
            "fecha": fecha_compra,
            "origen_nombre": proveedor,
            "origen_identificacion": documento_compra,
            "observaciones": observaciones,
        },
    )

    adquisicion = Adquisicion.objects.create(
        finca=finca,
        proveedor=proveedor,
        fecha=fecha_compra,
        numero_documento=documento_compra,
        costo_total=precio_individual,
        observaciones=observaciones,
    )
    AdquisicionAnimal.objects.create(
        adquisicion=adquisicion,
        animal=animal,
        precio_individual=precio_individual,
        observaciones=observaciones,
    )

    if peso_inicial is not None:
        PesajeAnimal.objects.create(
            animal=animal,
            fecha=fecha_compra,
            peso_kg=peso_inicial,
            observaciones="Peso inicial de ingreso.",
        )

    if potrero_inicial is not None:
        MovimientoAnimal.objects.create(
            animal=animal,
            potrero=potrero_inicial,
            fecha_entrada=fecha_compra,
            activo=True,
            observaciones="Ubicación inicial registrada durante el ingreso.",
        )

    return animal


@transaction.atomic
def registrar_ingreso_nacimiento(*, finca, animal, madre, padre=None, fecha_parto, tipo_parto, peso_inicial=None, potrero_inicial=None, observaciones="", creado_por=None):
    animal.finca = finca
    animal.madre = madre
    animal.padre = padre
    animal.fecha_nacimiento = fecha_parto.date()
    animal.save()

    ProcedenciaAnimal.objects.update_or_create(
        animal=animal,
        defaults={
            "tipo": "nacimiento_granja",
            "fecha": fecha_parto.date(),
            "origen_nombre": madre.nombre_propio or madre.numero_arete,
            "origen_identificacion": madre.numero_arete,
            "observaciones": observaciones,
        },
    )

    parto = EventoReproductivo.objects.create(
        finca=finca,
        animal=madre,
        tipo_evento="parto",
        fecha=fecha_parto,
        toro=padre,
        tipo_parto=tipo_parto,
        creado_por=creado_por,
        observaciones=observaciones,
    )

    CriaNacimiento.objects.create(
        finca=finca,
        parto=parto,
        animal=animal,
        creado_por=creado_por,
        observaciones=observaciones,
    )

    if peso_inicial is not None:
        PesajeAnimal.objects.create(
            animal=animal,
            fecha=fecha_parto,
            peso_kg=peso_inicial,
            observaciones="Peso al nacimiento.",
        )

    if potrero_inicial is not None:
        MovimientoAnimal.objects.create(
            animal=animal,
            potrero=potrero_inicial,
            fecha_entrada=fecha_parto,
            activo=True,
            observaciones="Ubicación inicial registrada durante el nacimiento.",
        )

    return animal

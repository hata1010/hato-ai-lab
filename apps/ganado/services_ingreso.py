from datetime import datetime, time

from django.db import transaction
from django.utils import timezone

from .models import (
    Adquisicion,
    AdquisicionAnimal,
    Animal,
    EventoSalud,
    MovimientoAnimal,
    PesajeAnimal,
    ProcedenciaAnimal,
)
from .models_reproduccion import CriaNacimiento, EventoReproductivo


def _fecha_ingreso_datetime(fecha):
    """Convierte una fecha de ingreso a un datetime consciente de zona horaria."""
    if isinstance(fecha, datetime):
        return fecha if timezone.is_aware(fecha) else timezone.make_aware(fecha)
    return timezone.make_aware(datetime.combine(fecha, time.min))


def _crear_evaluacion_salud(*, animal, tipo, fecha, veterinario="", observaciones=""):
    if not tipo or not fecha:
        return None
    fecha_dt = fecha if isinstance(fecha, datetime) else _fecha_ingreso_datetime(fecha)
    return EventoSalud.objects.create(
        animal=animal,
        tipo=tipo,
        fecha=fecha_dt,
        nombre_veterinario=veterinario,
        observaciones=observaciones,
    )


@transaction.atomic
def registrar_ingreso_compra(*, finca, animal, proveedor, fecha_compra, documento_compra="", precio_individual=None, peso_inicial=None, potrero_inicial=None, salud_inicial_tipo="", salud_inicial_fecha=None, salud_inicial_veterinario="", salud_inicial_observaciones="", observaciones=""):
    animal.finca = finca
    animal.save()
    fecha_ingreso = _fecha_ingreso_datetime(fecha_compra)

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
            fecha=fecha_ingreso,
            peso_kg=peso_inicial,
            observaciones="Peso inicial de ingreso.",
        )

    if potrero_inicial is not None:
        MovimientoAnimal.objects.create(
            animal=animal,
            potrero=potrero_inicial,
            fecha_entrada=fecha_ingreso,
            activo=True,
            observaciones="Ubicación inicial registrada durante el ingreso.",
        )

    _crear_evaluacion_salud(
        animal=animal,
        tipo=salud_inicial_tipo,
        fecha=salud_inicial_fecha,
        veterinario=salud_inicial_veterinario,
        observaciones=salud_inicial_observaciones,
    )

    return animal


@transaction.atomic
def registrar_ingreso_nacimiento(*, finca, animal, madre, padre=None, fecha_parto, tipo_parto, peso_inicial=None, potrero_inicial=None, salud_inicial_tipo="", salud_inicial_fecha=None, salud_inicial_veterinario="", salud_inicial_observaciones="", observaciones="", creado_por=None):
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

    _crear_evaluacion_salud(
        animal=animal,
        tipo=salud_inicial_tipo,
        fecha=salud_inicial_fecha,
        veterinario=salud_inicial_veterinario,
        observaciones=salud_inicial_observaciones,
    )

    return animal

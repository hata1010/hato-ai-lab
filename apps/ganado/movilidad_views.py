from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.core.tenant import obtener_finca_activa, obtener_rol_usuario_finca, verificar_acceso_finca
from apps.core.models import Potrero

from .models import Animal, MovimientoAnimal, PesajeAnimal
from .movilidad_forms import CambioPotreroForm, MovimientoAnimalForm


ROLES_GESTION_MOVILIDAD = {"superusuario", "propietario", "administrador"}


def _finca_activa_o_denegar(request):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes autorización sobre una finca activa.")
    return finca


def _puede_gestionar(request, finca):
    return obtener_rol_usuario_finca(request.user, finca) in ROLES_GESTION_MOVILIDAD


def _ultimos_pesos(animal_ids):
    pesos = {}
    if not animal_ids:
        return pesos
    for pesaje in PesajeAnimal.objects.filter(animal_id__in=animal_ids).order_by("animal_id", "-fecha"):
        pesos.setdefault(pesaje.animal_id, pesaje.peso_kg)
    return pesos


def _datos_tablero_movilidad(finca):
    """Construye la representación operacional del tablero sin alterar modelos."""
    potreros = list(
        Potrero.objects.filter(finca=finca, is_active=True).order_by("nombre")
    )
    movimientos_activos = list(
        MovimientoAnimal.objects.filter(animal__finca=finca, activo=True)
        .select_related("animal", "potrero")
        .order_by("animal__numero_arete")
    )

    animal_ids = [movimiento.animal_id for movimiento in movimientos_activos]
    pesos = _ultimos_pesos(animal_ids)
    por_potrero = {potrero.id: [] for potrero in potreros}
    ubicados = set()

    for movimiento in movimientos_activos:
        movimiento.animal.ultimo_peso = pesos.get(movimiento.animal_id)
        if movimiento.potrero_id in por_potrero:
            por_potrero[movimiento.potrero_id].append(movimiento)
            ubicados.add(movimiento.animal_id)

    tarjetas = []
    for potrero in potreros:
        animales = por_potrero[potrero.id]
        capacidad = potrero.capacidad_animales
        cantidad = len(animales)
        porcentaje = min(round((cantidad / capacidad) * 100), 100) if capacidad else None
        tarjetas.append({
            "potrero": potrero,
            "movimientos": animales,
            "cantidad": cantidad,
            "capacidad": capacidad,
            "porcentaje": porcentaje,
        })

    sin_ubicacion = list(
        Animal.objects.filter(finca=finca, is_active=True)
        .exclude(id__in=ubicados)
        .order_by("numero_arete")
    )
    sin_pesos = _ultimos_pesos([animal.id for animal in sin_ubicacion])
    for animal in sin_ubicacion:
        animal.ultimo_peso = sin_pesos.get(animal.id)

    return tarjetas, sin_ubicacion


@login_required
def lista_movilidad(request):
    finca = _finca_activa_o_denegar(request)
    consulta = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()

    tarjetas, sin_ubicacion = _datos_tablero_movilidad(finca)

    if consulta:
        consulta_lower = consulta.lower()
        for tarjeta in tarjetas:
            tarjeta["movimientos"] = [
                movimiento for movimiento in tarjeta["movimientos"]
                if consulta_lower in movimiento.animal.numero_arete.lower()
                or consulta_lower in movimiento.animal.nombre_propio.lower()
            ]
            tarjeta["cantidad"] = len(tarjeta["movimientos"])
            capacidad = tarjeta["capacidad"]
            tarjeta["porcentaje"] = min(round((tarjeta["cantidad"] / capacidad) * 100), 100) if capacidad else None
        sin_ubicacion = [
            animal for animal in sin_ubicacion
            if consulta_lower in animal.numero_arete.lower()
            or consulta_lower in animal.nombre_propio.lower()
        ]

    movimientos = (
        MovimientoAnimal.objects.filter(animal__finca=finca)
        .select_related("animal", "potrero")
        .order_by("-fecha_entrada")
    )
    if consulta:
        movimientos = movimientos.filter(
            animal__numero_arete__icontains=consulta
        ) | movimientos.filter(
            animal__nombre_propio__icontains=consulta
        ) | movimientos.filter(
            potrero__nombre__icontains=consulta
        )
    if estado == "activos":
        movimientos = movimientos.filter(activo=True)
    elif estado == "cerrados":
        movimientos = movimientos.filter(activo=False)

    return render(request, "ganado/movilidad_lista.html", {
        "finca": finca,
        "movimientos": movimientos.distinct(),
        "consulta": consulta,
        "estado_actual": estado,
        "puede_gestionar": _puede_gestionar(request, finca),
        "rol": obtener_rol_usuario_finca(request.user, finca),
        "potrero_tarjetas": tarjetas,
        "sin_ubicacion": sin_ubicacion,
    })


@login_required
def historial_movilidad_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    animal = get_object_or_404(Animal, id=animal_id, finca=finca)
    movimientos = animal.movimientos.select_related("potrero", "tipo_pasto").order_by("-fecha_entrada")
    return render(request, "ganado/movilidad_animal.html", {
        "finca": finca,
        "animal": animal,
        "movimientos": movimientos,
        "puede_gestionar": _puede_gestionar(request, finca),
        "rol": obtener_rol_usuario_finca(request.user, finca),
    })


@login_required
def crear_movimiento(request):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar(request, finca):
        raise PermissionDenied("Tu rol no permite gestionar la movilidad del ganado.")
    initial = {}
    animal_id = request.GET.get("animal")
    if animal_id:
        initial["animal"] = get_object_or_404(Animal, id=animal_id, finca=finca)
    form = MovimientoAnimalForm(request.POST or None, finca=finca, initial=initial)
    if request.method == "POST" and form.is_valid():
        movimiento = form.save(commit=False)
        if movimiento.animal.finca_id != finca.id or movimiento.potrero.finca_id != finca.id:
            raise PermissionDenied("Animal y potrero deben pertenecer a la finca activa.")
        movimiento.activo = True
        movimiento.fecha_salida = None
        movimiento.save()
        messages.success(request, "Movimiento registrado correctamente.")
        return redirect("ganado:detalle_animal", animal_id=movimiento.animal_id)
    return render(request, "ganado/movilidad_form.html", {
        "finca": finca, "form": form, "modo": "crear",
        "rol": obtener_rol_usuario_finca(request.user, finca),
    })


@login_required
def cambiar_potrero(request, movimiento_id):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar(request, finca):
        raise PermissionDenied("Tu rol no permite cambiar el potrero del ganado.")

    movimiento = get_object_or_404(
        MovimientoAnimal.objects.select_related("animal", "potrero"),
        id=movimiento_id,
        animal__finca=finca,
        activo=True,
    )
    form = CambioPotreroForm(
        request.POST or None,
        finca=finca,
        potrero_actual=movimiento.potrero,
        initial={"fecha_entrada": timezone.localtime().strftime("%Y-%m-%dT%H:%M")},
    )

    if request.method == "POST" and form.is_valid():
        fecha_cambio = form.cleaned_data["fecha_entrada"]
        if fecha_cambio < movimiento.fecha_entrada:
            form.add_error("fecha_entrada", "La fecha del cambio no puede ser anterior a la entrada actual.")
        else:
            with transaction.atomic():
                movimiento.fecha_salida = fecha_cambio
                movimiento.activo = False
                movimiento.save(update_fields=["fecha_salida", "activo"])
                MovimientoAnimal.objects.create(
                    animal=movimiento.animal,
                    potrero=form.cleaned_data["potrero"],
                    fecha_entrada=fecha_cambio,
                    activo=True,
                    observaciones=form.cleaned_data["observaciones"],
                )
            messages.success(request, "Cambio de potrero registrado y movimiento anterior cerrado correctamente.")
            return redirect("ganado:historial_movilidad_animal", animal_id=movimiento.animal_id)

    return render(request, "ganado/cambio_potrero_form.html", {
        "finca": finca,
        "movimiento": movimiento,
        "form": form,
        "rol": obtener_rol_usuario_finca(request.user, finca),
    })


@login_required
def cerrar_movimiento(request, movimiento_id):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar(request, finca):
        raise PermissionDenied("Tu rol no permite cerrar movimientos.")
    movimiento = get_object_or_404(
        MovimientoAnimal.objects.select_related("animal", "potrero"),
        id=movimiento_id, animal__finca=finca, activo=True,
    )
    if request.method != "POST":
        return render(request, "ganado/movilidad_cerrar.html", {"finca": finca, "movimiento": movimiento})
    movimiento.fecha_salida = timezone.now()
    movimiento.activo = False
    movimiento.save(update_fields=["fecha_salida", "activo"])
    messages.success(request, "Movimiento cerrado correctamente.")
    return redirect("ganado:historial_movilidad_animal", animal_id=movimiento.animal_id)

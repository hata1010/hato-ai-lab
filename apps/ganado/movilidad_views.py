from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.core.tenant import obtener_finca_activa, obtener_rol_usuario_finca, verificar_acceso_finca

from .models import Animal, MovimientoAnimal
from .movilidad_forms import MovimientoAnimalForm


ROLES_GESTION_MOVILIDAD = {"superusuario", "propietario", "administrador"}


def _finca_activa_o_denegar(request):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes autorización sobre una finca activa.")
    return finca


def _puede_gestionar(request, finca):
    return obtener_rol_usuario_finca(request.user, finca) in ROLES_GESTION_MOVILIDAD


@login_required
def lista_movilidad(request):
    finca = _finca_activa_o_denegar(request)
    movimientos = (
        MovimientoAnimal.objects.filter(animal__finca=finca)
        .select_related("animal", "potrero")
        .order_by("-fecha_entrada")
    )
    consulta = request.GET.get("q", "").strip()
    if consulta:
        movimientos = movimientos.filter(animal__numero_arete__icontains=consulta) | movimientos.filter(
            animal__nombre_propio__icontains=consulta
        ) | movimientos.filter(potrero__nombre__icontains=consulta)
    estado = request.GET.get("estado", "").strip()
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

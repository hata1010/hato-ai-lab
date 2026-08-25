from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import PotreroForm
from .models import Potrero
from .tenant import obtener_finca_activa, obtener_rol_usuario_finca, verificar_acceso_finca


ROLES_GESTION = {"superusuario", "propietario", "administrador"}


def _finca_y_permiso(request, gestionar=False):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes una finca activa autorizada.")
    rol = obtener_rol_usuario_finca(request.user, finca)
    if gestionar and rol not in ROLES_GESTION:
        raise PermissionDenied("Tu rol no permite gestionar potreros.")
    return finca, rol


@login_required

def lista_potreros(request):
    finca, rol = _finca_y_permiso(request)
    potreros = Potrero.objects.filter(finca=finca)
    return render(
        request,
        "core/potreros_lista.html",
        {"finca": finca, "rol": rol, "potreros": potreros, "puede_gestionar": rol in ROLES_GESTION},
    )


@login_required

def detalle_potrero(request, potrero_id):
    finca, rol = _finca_y_permiso(request)
    potrero = get_object_or_404(Potrero, id=potrero_id, finca=finca)
    return render(
        request,
        "core/potrero_detalle.html",
        {"finca": finca, "rol": rol, "potrero": potrero, "puede_gestionar": rol in ROLES_GESTION},
    )


@login_required
@require_http_methods(["GET", "POST"])
def crear_potrero(request):
    finca, _ = _finca_y_permiso(request, gestionar=True)
    form = PotreroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        potrero = form.save(commit=False)
        potrero.finca = finca
        potrero.save()
        messages.success(request, f"Potrero «{potrero.nombre}» creado correctamente.")
        return redirect("potreros:detalle", potrero_id=potrero.id)
    return render(request, "core/potrero_form.html", {"finca": finca, "form": form, "titulo": "Nuevo potrero"})


@login_required
@require_http_methods(["GET", "POST"])
def editar_potrero(request, potrero_id):
    finca, _ = _finca_y_permiso(request, gestionar=True)
    potrero = get_object_or_404(Potrero, id=potrero_id, finca=finca)
    form = PotreroForm(request.POST or None, instance=potrero, potrero=potrero)
    if request.method == "POST" and form.is_valid():
        potrero = form.save()
        messages.success(request, f"Potrero «{potrero.nombre}» actualizado correctamente.")
        return redirect("potreros:detalle", potrero_id=potrero.id)
    return render(request, "core/potrero_form.html", {"finca": finca, "form": form, "potrero": potrero, "titulo": "Editar potrero"})


@login_required
@require_http_methods(["POST"])
def eliminar_potrero(request, potrero_id):
    finca, _ = _finca_y_permiso(request, gestionar=True)
    potrero = get_object_or_404(Potrero, id=potrero_id, finca=finca)
    nombre = potrero.nombre
    potrero.delete()
    messages.success(request, f"Potrero «{nombre}» eliminado correctamente.")
    return redirect("potreros:lista")

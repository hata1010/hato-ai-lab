from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.tenant import (
    obtener_finca_activa,
    obtener_rol_usuario_finca,
    verificar_acceso_finca,
)

from .forms import PesajeAnimalForm
from .models import Animal, PesajeAnimal


ROLES_GESTION_PESAJES = {"superusuario", "propietario", "administrador"}


def _finca_activa_o_denegar(request):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes autorización sobre una finca activa.")
    return finca


def _puede_gestionar_pesajes(request, finca):
    return obtener_rol_usuario_finca(request.user, finca) in ROLES_GESTION_PESAJES


@login_required
def lista_pesajes(request):
    finca = _finca_activa_o_denegar(request)
    pesajes = PesajeAnimal.objects.filter(animal__finca=finca).select_related("animal").order_by("-fecha")
    consulta = request.GET.get("q", "").strip()
    if consulta:
        pesajes = pesajes.filter(animal__numero_arete__icontains=consulta)
    return render(request, "ganado/pesajes_lista.html", {
        "finca": finca,
        "pesajes": pesajes,
        "consulta": consulta,
        "puede_gestionar": _puede_gestionar_pesajes(request, finca),
        "rol": obtener_rol_usuario_finca(request.user, finca),
    })


@login_required
def historial_pesajes_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    animal = get_object_or_404(Animal, id=animal_id, finca=finca)
    return render(request, "ganado/pesajes_historial.html", {
        "finca": finca,
        "animal": animal,
        "pesajes": animal.pesajes.all(),
        "puede_gestionar": _puede_gestionar_pesajes(request, finca),
        "rol": obtener_rol_usuario_finca(request.user, finca),
    })


@login_required
def crear_pesaje(request):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_pesajes(request, finca):
        raise PermissionDenied("Tu rol no permite registrar pesajes.")
    animal_id = request.GET.get("animal") or request.POST.get("animal")
    animal = get_object_or_404(Animal, id=animal_id, finca=finca) if animal_id else None
    form = PesajeAnimalForm(request.POST or None, finca=finca, animal=animal)
    if request.method == "POST" and form.is_valid():
        pesaje = form.save()
        messages.success(request, f"Pesaje de {pesaje.animal.numero_arete} registrado correctamente.")
        return redirect("ganado:historial_pesajes_animal", animal_id=pesaje.animal_id)
    return render(request, "ganado/pesaje_form.html", {
        "finca": finca,
        "form": form,
        "animal": animal,
        "rol": obtener_rol_usuario_finca(request.user, finca),
    })

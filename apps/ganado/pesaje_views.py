from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.tenant import (
    obtener_finca_activa,
    obtener_rol_usuario_finca,
    verificar_acceso_finca,
)

from .models import Animal, PesajeAnimal
from .pesaje_forms import PesajeAnimalForm


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
    pesajes = (
        PesajeAnimal.objects.filter(animal__finca=finca)
        .select_related("animal")
        .order_by("-fecha")
    )

    consulta = request.GET.get("q", "").strip()
    if consulta:
        pesajes = pesajes.filter(
            animal__numero_arete__icontains=consulta
        ) | pesajes.filter(
            animal__nombre_propio__icontains=consulta
        )

    return render(
        request,
        "ganado/pesajes_lista.html",
        {
            "finca": finca,
            "pesajes": pesajes.distinct(),
            "consulta": consulta,
            "puede_gestionar": _puede_gestionar_pesajes(request, finca),
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def crear_pesaje(request):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_pesajes(request, finca):
        raise PermissionDenied("Tu rol no permite registrar pesajes.")

    initial = {}
    animal_id = request.GET.get("animal")
    if animal_id:
        initial["animal"] = get_object_or_404(Animal, id=animal_id, finca=finca)

    form = PesajeAnimalForm(request.POST or None, finca=finca, initial=initial)
    if request.method == "POST" and form.is_valid():
        pesaje = form.save(commit=False)
        if pesaje.animal.finca_id != finca.id:
            raise PermissionDenied("El animal no pertenece a la finca activa.")
        pesaje.save()
        messages.success(request, "Pesaje registrado correctamente.")
        return redirect("ganado:detalle_animal", animal_id=pesaje.animal_id)

    return render(
        request,
        "ganado/pesaje_form.html",
        {
            "finca": finca,
            "form": form,
            "modo": "crear",
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def editar_pesaje(request, pesaje_id):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_pesajes(request, finca):
        raise PermissionDenied("Tu rol no permite modificar pesajes.")

    pesaje = get_object_or_404(
        PesajeAnimal.objects.select_related("animal"),
        id=pesaje_id,
        animal__finca=finca,
    )
    form = PesajeAnimalForm(request.POST or None, instance=pesaje, finca=finca)
    if request.method == "POST" and form.is_valid():
        pesaje = form.save(commit=False)
        if pesaje.animal.finca_id != finca.id:
            raise PermissionDenied("El animal no pertenece a la finca activa.")
        pesaje.save()
        messages.success(request, "Pesaje actualizado correctamente.")
        return redirect("ganado:detalle_animal", animal_id=pesaje.animal_id)

    return render(
        request,
        "ganado/pesaje_form.html",
        {
            "finca": finca,
            "form": form,
            "pesaje": pesaje,
            "modo": "editar",
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def historial_pesajes_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    animal = get_object_or_404(Animal, id=animal_id, finca=finca)
    pesajes = animal.pesajes.all().order_by("-fecha")
    return render(
        request,
        "ganado/pesajes_animal.html",
        {
            "finca": finca,
            "animal": animal,
            "pesajes": pesajes,
            "puede_gestionar": _puede_gestionar_pesajes(request, finca),
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )

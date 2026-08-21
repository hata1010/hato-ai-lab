from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.tenant import (
    obtener_finca_activa,
    obtener_rol_usuario_finca,
    verificar_acceso_finca,
)

from .forms import AnimalForm
from .models import Animal


ROLES_GESTION_ANIMALES = {"superusuario", "propietario", "administrador"}


def _finca_activa_o_denegar(request):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes autorización sobre una finca activa.")
    return finca


def _puede_gestionar_animales(request, finca):
    return obtener_rol_usuario_finca(request.user, finca) in ROLES_GESTION_ANIMALES


@login_required
def lista_animales(request):
    finca = _finca_activa_o_denegar(request)
    animales = (
        Animal.objects
        .filter(finca=finca)
        .select_related("especie", "raza_declarada", "padre", "madre")
        .order_by("numero_arete")
    )

    consulta = request.GET.get("q", "").strip()
    if consulta:
        animales = animales.filter(numero_arete__icontains=consulta) | animales.filter(nombre_propio__icontains=consulta)

    estado = request.GET.get("estado", "").strip()
    if estado:
        animales = animales.filter(estado=estado)

    sexo = request.GET.get("sexo", "").strip()
    if sexo:
        animales = animales.filter(sexo=sexo)

    return render(
        request,
        "ganado/animales_lista.html",
        {
            "finca": finca,
            "animales": animales.distinct(),
            "puede_gestionar": _puede_gestionar_animales(request, finca),
            "consulta": consulta,
            "estado_actual": estado,
            "sexo_actual": sexo,
            "estados": Animal.ESTADO_CHOICES,
            "sexos": Animal.SEXO_CHOICES,
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def detalle_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    animal = get_object_or_404(
        Animal.objects.select_related("especie", "raza_declarada", "padre", "madre"),
        id=animal_id,
        finca=finca,
    )

    return render(
        request,
        "ganado/animal_detalle.html",
        {
            "finca": finca,
            "animal": animal,
            "puede_gestionar": _puede_gestionar_animales(request, finca),
            "movimientos": animal.movimientos.select_related("potrero", "tipo_pasto").all(),
            "pesajes": animal.pesajes.all(),
            "eventos_salud": animal.eventos_salud.all(),
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def crear_animal(request):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_animales(request, finca):
        raise PermissionDenied("Tu rol no permite registrar animales.")

    form = AnimalForm(request.POST or None, finca=finca)
    if request.method == "POST" and form.is_valid():
        animal = form.save(commit=False)
        animal.finca = finca
        animal.save()
        messages.success(request, f"Animal {animal.numero_arete} registrado correctamente.")
        return redirect("ganado:detalle_animal", animal_id=animal.id)

    return render(
        request,
        "ganado/animal_form.html",
        {"finca": finca, "form": form, "modo": "crear", "rol": obtener_rol_usuario_finca(request.user, finca)},
    )


@login_required
def editar_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_animales(request, finca):
        raise PermissionDenied("Tu rol no permite modificar animales.")

    animal = get_object_or_404(Animal, id=animal_id, finca=finca)
    form = AnimalForm(request.POST or None, instance=animal, finca=finca)

    if request.method == "POST" and form.is_valid():
        animal = form.save(commit=False)
        animal.finca = finca
        animal.save()
        messages.success(request, f"Animal {animal.numero_arete} actualizado correctamente.")
        return redirect("ganado:detalle_animal", animal_id=animal.id)

    return render(
        request,
        "ganado/animal_form.html",
        {"finca": finca, "form": form, "animal": animal, "modo": "editar", "rol": obtener_rol_usuario_finca(request.user, finca)},
    )

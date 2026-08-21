from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.tenant import (
    obtener_finca_activa,
    obtener_rol_usuario_finca,
    verificar_acceso_finca,
)

from .models import Animal, EventoSalud
from .salud_forms import EventoSaludForm


ROLES_GESTION_SALUD = {"superusuario", "propietario", "administrador"}


def _finca_activa_o_denegar(request):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        raise PermissionDenied("No tienes autorización sobre una finca activa.")
    return finca


def _puede_gestionar_salud(request, finca):
    return obtener_rol_usuario_finca(request.user, finca) in ROLES_GESTION_SALUD


@login_required
def lista_salud(request):
    finca = _finca_activa_o_denegar(request)
    eventos = (
        EventoSalud.objects.filter(animal__finca=finca)
        .select_related("animal")
        .order_by("-fecha")
    )

    consulta = request.GET.get("q", "").strip()
    if consulta:
        eventos = eventos.filter(
            animal__numero_arete__icontains=consulta
        ) | eventos.filter(
            animal__nombre_propio__icontains=consulta
        ) | eventos.filter(
            producto__icontains=consulta
        ) | eventos.filter(
            nombre_veterinario__icontains=consulta
        )

    tipo = request.GET.get("tipo", "").strip()
    if tipo:
        eventos = eventos.filter(tipo=tipo)

    return render(
        request,
        "ganado/salud_lista.html",
        {
            "finca": finca,
            "eventos": eventos.distinct(),
            "tipos": EventoSalud.TIPO_CHOICES,
            "tipo_actual": tipo,
            "consulta": consulta,
            "puede_gestionar": _puede_gestionar_salud(request, finca),
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def historia_salud_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    animal = get_object_or_404(
        Animal.objects.select_related("especie", "raza_declarada"),
        id=animal_id,
        finca=finca,
    )
    eventos = animal.eventos_salud.all().order_by("-fecha")
    return render(
        request,
        "ganado/salud_historia.html",
        {
            "finca": finca,
            "animal": animal,
            "eventos": eventos,
            "puede_gestionar": _puede_gestionar_salud(request, finca),
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def crear_evento_salud(request):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_salud(request, finca):
        raise PermissionDenied("Tu rol no permite registrar eventos de salud.")

    initial = {}
    animal_id = request.GET.get("animal")
    if animal_id:
        animal = get_object_or_404(Animal, id=animal_id, finca=finca)
        initial["animal"] = animal

    form = EventoSaludForm(request.POST or None, finca=finca, initial=initial)
    if request.method == "POST" and form.is_valid():
        evento = form.save(commit=False)
        if evento.animal.finca_id != finca.id:
            raise PermissionDenied("El animal no pertenece a la finca activa.")
        evento.save()
        messages.success(request, "Evento de salud registrado correctamente.")
        return redirect("ganado:historia_salud_animal", animal_id=evento.animal_id)

    return render(
        request,
        "ganado/salud_form.html",
        {
            "finca": finca,
            "form": form,
            "modo": "crear",
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )


@login_required
def editar_evento_salud(request, evento_id):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_salud(request, finca):
        raise PermissionDenied("Tu rol no permite modificar eventos de salud.")

    evento = get_object_or_404(
        EventoSalud.objects.select_related("animal"),
        id=evento_id,
        animal__finca=finca,
    )
    form = EventoSaludForm(request.POST or None, instance=evento, finca=finca)
    if request.method == "POST" and form.is_valid():
        evento = form.save(commit=False)
        if evento.animal.finca_id != finca.id:
            raise PermissionDenied("El animal no pertenece a la finca activa.")
        evento.save()
        messages.success(request, "Evento de salud actualizado correctamente.")
        return redirect("ganado:historia_salud_animal", animal_id=evento.animal_id)

    return render(
        request,
        "ganado/salud_form.html",
        {
            "finca": finca,
            "form": form,
            "evento": evento,
            "modo": "editar",
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )

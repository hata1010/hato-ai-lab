from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.core.tenant import (
    obtener_finca_activa,
    obtener_rol_usuario_finca,
    verificar_acceso_finca,
)

from .animal_edit_form import AnimalEditForm
from .forms import IngresoAnimalForm
from .models import Animal
from .services_ingreso import registrar_ingreso_compra, registrar_ingreso_nacimiento


ROLES_GESTION_ANIMALES = {"superusuario", "propietario", "administrador"}
ANIMALES_POR_PAGINA = 25


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

    animales = animales.distinct()
    paginator = Paginator(animales, ANIMALES_POR_PAGINA)
    pagina = paginator.get_page(request.GET.get("page", 1))

    parametros_paginacion = request.GET.copy()
    parametros_paginacion.pop("page", None)

    return render(
        request,
        "ganado/animales_lista.html",
        {
            "finca": finca,
            "animales": pagina.object_list,
            "pagina": pagina,
            "paginator": paginator,
            "parametros_paginacion": parametros_paginacion.urlencode(),
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

    form = IngresoAnimalForm(request.POST or None, finca=finca)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                animal = form.save(commit=False)
                animal.finca = finca
                origen = form.cleaned_data["origen"]
                salud = {
                    "salud_inicial_tipo": form.cleaned_data.get("salud_inicial_tipo", ""),
                    "salud_inicial_fecha": form.cleaned_data.get("salud_inicial_fecha"),
                    "salud_inicial_veterinario": form.cleaned_data.get("salud_inicial_veterinario", ""),
                    "salud_inicial_observaciones": form.cleaned_data.get("salud_inicial_observaciones", ""),
                }

                if origen == "nacimiento_granja":
                    animal = registrar_ingreso_nacimiento(
                        finca=finca,
                        animal=animal,
                        madre=form.cleaned_data["madre"],
                        padre=form.cleaned_data.get("padre"),
                        fecha_parto=form.cleaned_data["fecha_parto"],
                        tipo_parto=form.cleaned_data["tipo_parto"],
                        peso_inicial=form.cleaned_data.get("peso_inicial"),
                        potrero_inicial=form.cleaned_data.get("potrero_inicial"),
                        observaciones=form.cleaned_data.get("observaciones", ""),
                        creado_por=request.user,
                        **salud,
                    )
                else:
                    animal = registrar_ingreso_compra(
                        finca=finca,
                        animal=animal,
                        proveedor=form.cleaned_data["proveedor"],
                        fecha_compra=form.cleaned_data["fecha_compra"],
                        documento_compra=form.cleaned_data.get("documento_compra", ""),
                        precio_individual=form.cleaned_data.get("precio_individual"),
                        peso_inicial=form.cleaned_data.get("peso_inicial"),
                        potrero_inicial=form.cleaned_data.get("potrero_inicial"),
                        observaciones=form.cleaned_data.get("observaciones", ""),
                        **salud,
                    )
            messages.success(request, f"Animal {animal.numero_arete} registrado correctamente.")
            return redirect("ganado:detalle_animal", animal_id=animal.id)
        except Exception as exc:
            form.add_error(None, f"No fue posible completar el ingreso: {exc}")

    return render(
        request,
        "ganado/animal_ingreso.html",
        {"finca": finca, "form": form, "rol": obtener_rol_usuario_finca(request.user, finca)},
    )


@login_required
def editar_animal(request, animal_id):
    finca = _finca_activa_o_denegar(request)
    if not _puede_gestionar_animales(request, finca):
        raise PermissionDenied("Tu rol no permite modificar animales.")

    animal = get_object_or_404(
        Animal.objects.select_related("especie", "raza_declarada", "padre", "madre"),
        id=animal_id,
        finca=finca,
    )

    form = AnimalEditForm(request.POST or None, instance=animal, finca=finca)

    if request.method == "POST" and form.is_valid():
        animal = form.save(commit=False)
        animal.finca = finca
        animal.save()
        messages.success(request, f"Animal {animal.numero_arete} actualizado correctamente.")
        return redirect("ganado:detalle_animal", animal_id=animal.id)

    return render(
        request,
        "ganado/animal_editar.html",
        {
            "finca": finca,
            "animal": animal,
            "form": form,
            "rol": obtener_rol_usuario_finca(request.user, finca),
        },
    )

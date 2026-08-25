from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.tenant import obtener_finca_activa, verificar_acceso_finca
from apps.ganado.models import Adquisicion


@login_required
def compras_adquisiciones(request):
    finca = obtener_finca_activa(request)
    if finca is None or not verificar_acceso_finca(request.user, finca):
        finca = None

    adquisiciones = []
    if finca:
        adquisiciones = (
            Adquisicion.objects.filter(finca=finca)
            .prefetch_related("animales__animal")
            .order_by("-fecha", "-id")
        )

    return render(
        request,
        "administrador/compras_adquisiciones.html",
        {
            "finca": finca,
            "adquisiciones": adquisiciones,
        },
    )

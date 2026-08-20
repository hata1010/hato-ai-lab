from django.shortcuts import render
from django.db.models import Sum, Q

from apps.core.tenant import obtener_finca_activa, obtener_fincas_usuario
from apps.ganado.models import Animal
from apps.core.models import Potrero
from apps.produccion.models import Metrica


def dashboard(request):
    """Portal de inicio y dashboard central de Hato AI Lab."""
    finca = obtener_finca_activa(request)
    fincas_usuario = obtener_fincas_usuario(request.user)

    total_animales = 0
    total_potreros = 0
    total_hectareas = 0
    total_metricas = 0
    ultimos_animales = []

    if finca:
        total_animales = Animal.objects.filter(
            finca=finca,
            estado="activo",
        ).count()

        potreros_qs = Potrero.objects.filter(
            finca=finca,
            is_active=True,
        )
        total_potreros = potreros_qs.count()
        total_hectareas = (
            potreros_qs.aggregate(total=Sum("area_hectareas"))["total"] or 0
        )

        # Incluye métricas propias de la finca y métricas globales activas.
        total_metricas = Metrica.objects.filter(
            Q(finca=finca) | Q(finca__isnull=True),
            activa=True,
        ).count()

        ultimos_animales = Animal.objects.filter(
            finca=finca,
        ).order_by("-id")[:5]

    contexto = {
        "titulo": "Portal Central — Hato AI Lab",
        "finca": finca,
        "fincas_disponibles": fincas_usuario,
        "total_animales": total_animales,
        "total_potreros": total_potreros,
        "total_hectareas": total_hectareas,
        "total_metricas": total_metricas,
        "ultimos_animales": ultimos_animales,
    }

    return render(
        request,
        "administrador/dashboard.html",
        contexto,
    )


def indicadores(request):
    finca = obtener_finca_activa(request)
    fincas_usuario = obtener_fincas_usuario(request.user)

    contexto = {
        "finca": finca,
        "fincas_disponibles": fincas_usuario,
    }
    return render(request, "administrador/indicadores.html", contexto)

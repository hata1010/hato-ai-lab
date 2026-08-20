from django.shortcuts import render
from apps.core.tenant import obtener_finca_activa, obtener_fincas_usuario
from apps.ganado.models import Animal
from apps.core.models import Potrero


def dashboard(request):
    finca = obtener_finca_activa(request)
    fincas_usuario = obtener_fincas_usuario(request.user)

    total_animales = 0
    total_potreros = 0

    if finca:
        total_animales = Animal.objects.filter(finca=finca, estado="activo").count()
        total_potreros = Potrero.objects.filter(finca=finca, is_active=True).count()

    contexto = {
        'titulo': 'Administración de la Finca',
        'finca': finca,
        'fincas_disponibles': fincas_usuario,
        'total_animales': total_animales,
        'total_potreros': total_potreros,
    }

    return render(
        request,
        'administrador/dashboard.html',
        contexto,
    )


def indicadores(request):
    finca = obtener_finca_activa(request)
    fincas_usuario = obtener_fincas_usuario(request.user)

    contexto = {
        'finca': finca,
        'fincas_disponibles': fincas_usuario,
    }
    return render(request, "administrador/indicadores.html", contexto)
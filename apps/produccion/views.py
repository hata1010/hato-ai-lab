from django.shortcuts import render
from apps.core.models import Finca
from apps.ganado.models import Animal
from apps.core.tenant import (
    obtener_finca_activa,
    obtener_fincas_usuario,
)
from apps.produccion.services.indicadores import (
    obtener_indicadores_finca,
)
from apps.produccion.engine.plan import PlanMetrica


def dashboard(request):
    finca = obtener_finca_activa(request)
    contexto = {
        "titulo": "Administración de la Finca",
        "finca": finca,
        "fincas_disponibles": obtener_fincas_usuario(request.user),
    }

    return render(
        request,
        "administrador/dashboard.html",
        contexto,
    )


def indicadores(request):
    finca = obtener_finca_activa(request)
    indicadores_list = []

    if finca:
        indicadores_list = obtener_indicadores_finca(finca=finca)

    contexto = {
        "finca": finca,
        "fincas_disponibles": obtener_fincas_usuario(request.user),
        "indicadores": indicadores_list,
    }

    return render(
        request,
        "administrador/indicadores.html",
        contexto,
    )


def prueba_motor(request):
    finca = obtener_finca_activa(request)
    fincas_disponibles = obtener_fincas_usuario(request.user)

    sexo = request.GET.get("sexo", "")
    metrica = request.GET.get("metrica", "peso_promedio")

    animales = Animal.objects.none()
    if finca:
        animales = Animal.objects.filter(finca=finca)

    pasos = []

    if sexo in ("H", "M"):
        pasos.append(
            {
                "funcion": "FILTRO",
                "parametros": {
                    "campo": "sexo",
                    "valor": sexo,
                },
            }
        )

    nombre_metrica = ""
    unidad = ""

    if metrica == "peso_promedio":
        pasos.extend(
            [
                {"funcion": "MAPEAR", "parametros": {"funcion": "PESO_ACTUAL"}},
                {"funcion": "PROMEDIO"},
            ]
        )
        nombre_metrica = "Peso promedio"
        unidad = "kg"

    elif metrica == "peso_total":
        pasos.extend(
            [
                {"funcion": "MAPEAR", "parametros": {"funcion": "PESO_ACTUAL"}},
                {"funcion": "SUMA"},
            ]
        )
        nombre_metrica = "Peso total"
        unidad = "kg"

    elif metrica == "cantidad":
        pasos.append({"funcion": "CONTEO"})
        nombre_metrica = "Cantidad de animales"
        unidad = "animales"

    else:
        metrica = "peso_promedio"
        pasos.extend(
            [
                {"funcion": "MAPEAR", "parametros": {"funcion": "PESO_ACTUAL"}},
                {"funcion": "PROMEDIO"},
            ]
        )
        nombre_metrica = "Peso promedio"
        unidad = "kg"

    plan = PlanMetrica(
        nombre=nombre_metrica,
        pasos=pasos,
    )

    validacion = plan.validar()
    resultado = None
    error = None

    if validacion.get("valido", False) and animales.exists():
        try:
            resultado = plan.ejecutar(animales)
        except Exception as exc:
            error = str(exc)

    explicacion = plan.explicar()

    nombres_sexo = {
        "": "Todos",
        "H": "Hembras",
        "M": "Machos",
    }
    sexo_nombre = nombres_sexo.get(sexo, "Todos")

    contexto = {
        "fincas": fincas_disponibles,
        "finca": finca,
        "sexo": sexo,
        "sexo_nombre": sexo_nombre,
        "metrica": metrica,
        "nombre_metrica": nombre_metrica,
        "unidad": unidad,
        "resultado": resultado,
        "error": error,
        "validacion": validacion,
        "explicacion": explicacion,
        "animales_count": animales.count(),
    }

    return render(
        request,
        "produccion/prueba_motor.html",
        contexto,
    )
from django.shortcuts import render, get_object_or_404

from apps.core.models import Finca
from apps.ganado.models import Animal

from apps.produccion.services.indicadores import (
    obtener_indicadores_finca,
)

from apps.produccion.engine.plan import PlanMetrica


# ============================================================
# DASHBOARD
# ============================================================

def dashboard(request):

    contexto = {
        "titulo": "Administración de la Finca",
    }

    return render(
        request,
        "administrador/dashboard.html",
        contexto,
    )


# ============================================================
# INDICADORES
# ============================================================

def indicadores(request):

    finca_id = request.GET.get("finca")

    if finca_id:
        finca = get_object_or_404(
            Finca,
            id=finca_id,
        )
    else:
        finca = Finca.objects.first()

    indicadores = obtener_indicadores_finca(
        finca=finca,
    )

    contexto = {
        "finca": finca,
        "indicadores": indicadores,
    }

    return render(
        request,
        "administrador/indicadores.html",
        contexto,
    )


# ============================================================
# PRUEBA TEMPORAL DEL MOTOR DE MÉTRICAS
# ============================================================

def prueba_motor(request):

    # --------------------------------------------------------
    # FINCAS
    # --------------------------------------------------------

    fincas = Finca.objects.all()

    finca_id = request.GET.get("finca")

    if finca_id:
        finca = get_object_or_404(
            Finca,
            id=finca_id,
        )
    else:
        finca = fincas.first()

    # --------------------------------------------------------
    # PARÁMETROS
    # --------------------------------------------------------

    sexo = request.GET.get(
        "sexo",
        "",
    )

    metrica = request.GET.get(
        "metrica",
        "peso_promedio",
    )

    # --------------------------------------------------------
    # ANIMALES DE LA FINCA
    # --------------------------------------------------------

    animales = Animal.objects.filter(
        finca=finca,
    )

    # --------------------------------------------------------
    # CONSTRUIR PLAN
    # --------------------------------------------------------

    pasos = []

    # --------------------------------------------------------
    # FILTRO POR SEXO
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # MÉTRICA
    # --------------------------------------------------------

    nombre_metrica = ""
    unidad = ""

    if metrica == "peso_promedio":

        pasos.extend(
            [
                {
                    "funcion": "MAPEAR",
                    "parametros": {
                        "funcion": "PESO_ACTUAL",
                    },
                },
                {
                    "funcion": "PROMEDIO",
                },
            ]
        )

        nombre_metrica = "Peso promedio"
        unidad = "kg"

    elif metrica == "peso_total":

        pasos.extend(
            [
                {
                    "funcion": "MAPEAR",
                    "parametros": {
                        "funcion": "PESO_ACTUAL",
                    },
                },
                {
                    "funcion": "SUMA",
                },
            ]
        )

        nombre_metrica = "Peso total"
        unidad = "kg"

    elif metrica == "cantidad":

        pasos.append(
            {
                "funcion": "CONTEO",
            }
        )

        nombre_metrica = "Cantidad de animales"
        unidad = "animales"

    else:

        metrica = "peso_promedio"

        pasos.extend(
            [
                {
                    "funcion": "MAPEAR",
                    "parametros": {
                        "funcion": "PESO_ACTUAL",
                    },
                },
                {
                    "funcion": "PROMEDIO",
                },
            ]
        )

        nombre_metrica = "Peso promedio"
        unidad = "kg"

    # --------------------------------------------------------
    # CREAR PLAN
    # --------------------------------------------------------

    plan = PlanMetrica(
        nombre=nombre_metrica,
        pasos=pasos,
    )

    # --------------------------------------------------------
    # VALIDAR
    # --------------------------------------------------------

    validacion = plan.validar()

    # --------------------------------------------------------
    # EJECUTAR
    # --------------------------------------------------------

    resultado = None
    error = None

    if validacion["valido"]:

        try:

            resultado = plan.ejecutar(
                animales,
            )

        except Exception as exc:

            error = str(exc)

    # --------------------------------------------------------
    # EXPLICACIÓN DEL MOTOR
    # --------------------------------------------------------

    explicacion = plan.explicar()

    # --------------------------------------------------------
    # NOMBRE DEL SEXO
    # --------------------------------------------------------

    nombres_sexo = {
        "": "Todos",
        "H": "Hembras",
        "M": "Machos",
    }

    sexo_nombre = nombres_sexo.get(
        sexo,
        "Todos",
    )

    # --------------------------------------------------------
    # CONTEXTO
    # --------------------------------------------------------

    contexto = {

        "fincas": fincas,

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
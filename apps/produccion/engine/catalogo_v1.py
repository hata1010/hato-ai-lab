"""Catálogo oficial de métricas preconstruidas V1 de Hato AI."""

from .definicion import DefinicionMetrica

METRICAS_V1 = {
    "CANT_ANIMALES_TOTAL": DefinicionMetrica(
        codigo="CANT_ANIMALES_TOTAL", nombre="Cantidad total de animales", tipo="atomica",
        familia="poblacion", unidad="animales", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"CONTEO"}]},
        descripcion="Cuenta el número total de animales registrados en la finca.",
    ),
    "CANT_ANIMALES_ACTIVOS": DefinicionMetrica(
        codigo="CANT_ANIMALES_ACTIVOS", nombre="Cantidad de animales activos", tipo="filtrada",
        familia="poblacion", unidad="animales", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[
            {"funcion":"FILTRO","parametros":{"campo":"estado","valor":"activo"}},
            {"funcion":"CONTEO"},
        ]},
        descripcion="Cuenta los animales en estado productivo activo.",
    ),
    "ANIMALES_POR_SEXO": DefinicionMetrica(
        codigo="ANIMALES_POR_SEXO", nombre="Animales por sexo", tipo="filtrada",
        familia="poblacion", unidad="animales", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[
            {"funcion":"FILTRO","parametros":{"campo":"sexo","valor":"H"}},
            {"funcion":"CONTEO"},
        ]},
        descripcion="Cuenta animales según su sexo (H o M).",
    ),
    "PESO_PROMEDIO_FINCA": DefinicionMetrica(
        codigo="PESO_PROMEDIO_FINCA", nombre="Peso promedio del rebaño", tipo="compuesta",
        familia="peso", unidad="kg", precision_decimales=2,
        estrategia={"modo":"pipeline","pasos":[
            {"funcion":"FILTRO","parametros":{"campo":"estado","valor":"activo"}},
            {"funcion":"MAPEAR","parametros":{"funcion":"PESO_ACTUAL"}},
            {"funcion":"PROMEDIO"},
        ]},
        descripcion="Media aritmética del último peso registrado de los animales activos.",
    ),
    "PESO_TOTAL_FINCA": DefinicionMetrica(
        codigo="PESO_TOTAL_FINCA", nombre="Biomasa total en pie", tipo="compuesta",
        familia="peso", unidad="kg", precision_decimales=2,
        estrategia={"modo":"pipeline","pasos":[
            {"funcion":"FILTRO","parametros":{"campo":"estado","valor":"activo"}},
            {"funcion":"MAPEAR","parametros":{"funcion":"PESO_ACTUAL"}},
            {"funcion":"SUMA"},
        ]},
        descripcion="Sumatoria del peso actual de los animales activos del rebaño.",
    ),
    "GMD_INDIVIDUAL": DefinicionMetrica(
        codigo="GMD_INDIVIDUAL", nombre="Ganancia media diaria individual", tipo="temporal",
        familia="crecimiento", unidad="kg/dia", precision_decimales=3,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"GMD_ANIMAL"}]},
        descripcion="Calcula la tasa de ganancia de peso diaria entre los dos últimos pesajes.",
    ),
    "SUP_TOTAL_POTREROS": DefinicionMetrica(
        codigo="SUP_TOTAL_POTREROS", nombre="Superficie total de potreros", tipo="atomica",
        familia="territorial", unidad="ha", precision_decimales=2,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"SUMA"}]},
        descripcion="Sumatoria de hectáreas de todos los potreros activos de la finca.",
    ),
    "CARGA_ANIMAL_HA": DefinicionMetrica(
        codigo="CARGA_ANIMAL_HA", nombre="Carga animal global", tipo="derivada",
        familia="capacidad_carga", unidad="cab/ha", precision_decimales=2,
        estrategia={"modo":"formula","formula":"animales / hectareas",
                    "dependencias":["CANT_ANIMALES_TOTAL","SUP_TOTAL_POTREROS"]},
        descripcion="Relación entre cabezas de ganado totales y hectáreas de pastoreo.",
    ),
    "IEP_ANIMAL": DefinicionMetrica(
        codigo="IEP_ANIMAL", nombre="Intervalo entre partos", tipo="temporal",
        familia="reproduccion", unidad="dias", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"IEP_ANIMAL"}]},
        descripcion="Días transcurridos entre los dos partos más recientes de una hembra.",
    ),
    "DIAS_ABIERTOS_ANIMAL": DefinicionMetrica(
        codigo="DIAS_ABIERTOS_ANIMAL", nombre="Días abiertos", tipo="temporal",
        familia="reproduccion", unidad="dias", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"DIAS_ABIERTOS_ANIMAL"}]},
        descripcion="Días entre el último parto y el primer diagnóstico de gestación positivo posterior registrado.",
    ),
    "LECHE_ACUM_LACTANCIA": DefinicionMetrica(
        codigo="LECHE_ACUM_LACTANCIA", nombre="Producción acumulada de lactancia", tipo="agregada",
        familia="lactancia", unidad="unidad_control", precision_decimales=3,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"LECHE_ACUM_LACTANCIA"}]},
        descripcion="Suma de los controles de una lactancia cuando toda la serie utiliza una única unidad explícita.",
    ),
    "DURACION_LACTANCIA": DefinicionMetrica(
        codigo="DURACION_LACTANCIA", nombre="Duración de lactancia", tipo="temporal",
        familia="lactancia", unidad="dias", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[{"funcion":"DURACION_LACTANCIA"}]},
        descripcion="Días entre inicio y fecha de secado de una lactancia cerrada.",
    ),
    "ANIMALES_NACIDOS": DefinicionMetrica(
        codigo="ANIMALES_NACIDOS", nombre="Animales nacidos", tipo="filtrada",
        familia="poblacion", unidad="animales", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[
            {"funcion":"FILTRO_PROCEDENCIA","parametros":{"valor":"nacimiento_granja"}},
            {"funcion":"CONTEO"},
        ]},
        descripcion="Cuenta los animales cuya procedencia registrada es nacimiento en la granja.",
    ),
    "ANIMALES_ADQUIRIDOS": DefinicionMetrica(
        codigo="ANIMALES_ADQUIRIDOS", nombre="Animales adquiridos", tipo="filtrada",
        familia="poblacion", unidad="animales", precision_decimales=0,
        estrategia={"modo":"pipeline","pasos":[
            {"funcion":"FILTRO_PROCEDENCIA","parametros":{"valor":"compra"}},
            {"funcion":"CONTEO"},
        ]},
        descripcion="Cuenta los animales cuya procedencia registrada es compra.",
    ),
}


def obtener_metrica_v1(codigo: str) -> DefinicionMetrica:
    try:
        return METRICAS_V1[codigo]
    except KeyError:
        raise ValueError(f"Métrica V1 no registrada en catálogo: {codigo}")

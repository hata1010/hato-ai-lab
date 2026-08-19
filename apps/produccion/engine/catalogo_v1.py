"""Catálogo oficial de las 8 métricas preconstruidas V1 de Hato AI."""

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
}

def obtener_metrica_v1(codigo: str) -> DefinicionMetrica:
    try:
        return METRICAS_V1[codigo]
    except KeyError:
        raise ValueError(f"Métrica V1 no registrada en catálogo: {codigo}")

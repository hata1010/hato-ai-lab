from apps.produccion.engine.evaluador import evaluar_metrica
from apps.produccion.engine.analizador import analizar_resultados
from apps.ganado.models import Animal

def obtener_indicador_metrica(metrica, animales):
    """
    Evalúa una métrica para un conjunto de animales
    y devuelve sus resultados junto con el análisis.
    """

    resultados = []

    for animal in animales:

        try:
            resultado = evaluar_metrica(
                metrica,
                animal,
            )

            resultado["animal"] = animal.numero_arete

            resultados.append(resultado)
            

        except Exception as e:
            resultados.append({
                "animal": animal.numero_arete,
                "error": str(e),
            })

    resultados_validos = [
        resultado
        for resultado in resultados
        if "resultado" in resultado
    ]

    if not resultados_validos:
        return {
            "metrica": metrica.codigo,
            "nombre": metrica.nombre,
            "resultados": resultados,
            "analisis": None,
        }

    analisis = analizar_resultados(
        resultados_validos
    )

    return {
        "metrica": metrica.codigo,
        "nombre": metrica.nombre,
        "unidad": metrica.unidad_resultado,
        "tipo_resultado": metrica.tipo_resultado,
        "resultados": resultados,
        "analisis": analisis,
    }
    
    

def obtener_indicadores_finca(
    finca,
    fecha_inicio=None,
    fecha_fin=None,
):
    """
    Obtiene todas las métricas activas de una finca
    y las evalúa sobre los animales de esa finca.
    """

    metricas = finca.metricas.filter(
        activa=True,
    )

    animales = Animal.objects.filter(
        finca=finca,
    )

    indicadores = []

    for metrica in metricas:

        indicador = obtener_indicador_metrica(
            metrica,
            animales,
        )

        indicadores.append(
            indicador
        )

    return indicadores
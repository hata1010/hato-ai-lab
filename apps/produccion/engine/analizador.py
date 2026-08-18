from decimal import Decimal


class ErrorAnalisisMetrica(Exception):
    pass


def analizar_resultados(resultados):

    if not resultados:
        raise ErrorAnalisisMetrica(
            "No existen resultados para analizar."
        )

    valores = []

    for resultado in resultados:

        valor = resultado.get("resultado")

        if valor is None:
            continue

        valores.append(
            Decimal(str(valor))
        )

    if not valores:
        raise ErrorAnalisisMetrica(
            "No existen resultados numericos para analizar."
        )

    total = len(valores)

    promedio = sum(valores) / total
    minimo = min(valores)
    maximo = max(valores)

    positivos = [
        valor
        for valor in valores
        if valor > 0
    ]

    negativos = [
        valor
        for valor in valores
        if valor < 0
    ]

    ceros = [
        valor
        for valor in valores
        if valor == 0
    ]

    return {
        "cantidad": total,
        "promedio": promedio,
        "minimo": minimo,
        "maximo": maximo,
        "positivos": len(positivos),
        "negativos": len(negativos),
        "ceros": len(ceros),
        "porcentaje_positivos": (
            Decimal(len(positivos) * 100) / total
        ),
        "porcentaje_negativos": (
            Decimal(len(negativos) * 100) / total
        ),
        "porcentaje_ceros": (
            Decimal(len(ceros) * 100) / total
        ),
    }

from .animal import PesoActual


from .agregacion import (
    Promedio,
    Suma,
    Conteo,
    Filtro,
)

from .mapa import Mapear

FUNCIONES = {
    PesoActual.codigo: PesoActual(),
    Promedio.codigo: Promedio(),
    Suma.codigo: Suma(),
    Conteo.codigo: Conteo(),
    Filtro.codigo: Filtro(),
    Mapear.codigo: Mapear(),
}


def obtener_funcion(codigo):
    """
    Obtiene una función del catálogo por su código.
    """

    try:
        return FUNCIONES[codigo]

    except KeyError:
        raise ValueError(
            f"Función no registrada: {codigo}"
        )
from .animal import PesoActual, GananciaMediaDiaria
from .agregacion import Promedio, Suma, Conteo, Filtro
from .mapa import Mapear

FUNCIONES = {
    PesoActual.codigo: PesoActual(),
    GananciaMediaDiaria.codigo: GananciaMediaDiaria(),
    Promedio.codigo: Promedio(),
    Suma.codigo: Suma(),
    Conteo.codigo: Conteo(),
    Filtro.codigo: Filtro(),
    Mapear.codigo: Mapear(),
}

def obtener_funcion(codigo):
    try:
        return FUNCIONES[codigo]
    except KeyError:
        raise ValueError(f"Función no registrada: {codigo}")

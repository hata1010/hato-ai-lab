from .animal import PesoActual, GananciaMediaDiaria
from .agregacion import Promedio, Suma, Conteo, Filtro
from .procedencia import FiltroProcedencia
from .mapa import Mapear
from .reproduccion_lactancia import (
    IntervaloEntrePartos,
    DiasAbiertos,
    ProduccionAcumuladaLactancia,
    DuracionLactancia,
)

FUNCIONES = {
    PesoActual.codigo: PesoActual(),
    GananciaMediaDiaria.codigo: GananciaMediaDiaria(),
    Promedio.codigo: Promedio(),
    Suma.codigo: Suma(),
    Conteo.codigo: Conteo(),
    Filtro.codigo: Filtro(),
    FiltroProcedencia.codigo: FiltroProcedencia(),
    Mapear.codigo: Mapear(),
    IntervaloEntrePartos.codigo: IntervaloEntrePartos(),
    DiasAbiertos.codigo: DiasAbiertos(),
    ProduccionAcumuladaLactancia.codigo: ProduccionAcumuladaLactancia(),
    DuracionLactancia.codigo: DuracionLactancia(),
}


def obtener_funcion(codigo):
    try:
        return FUNCIONES[codigo]
    except KeyError:
        raise ValueError(f"Función no registrada: {codigo}")

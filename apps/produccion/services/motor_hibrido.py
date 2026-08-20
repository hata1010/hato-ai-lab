"""Fachada de ejecución híbrida para el Motor de Métricas.

M05 unifica las dos fuentes de definiciones:
1. métricas configuradas en BD por el administrador;
2. métricas preinstaladas en catalogo_v1.py.

La ejecución sigue siendo responsabilidad exclusiva de EjecutorMotorV1.
"""

from apps.produccion.engine.catalogo_v1 import obtener_metrica_v1
from apps.produccion.engine.ejecutor import EjecutorMotorV1
from apps.produccion.services.descubrimiento import (
    DescubridorMetricas,
    MetricaNoDisponible,
)


class MetricaNoEncontrada(Exception):
    """No existe una definición configurable ni preinstalada."""


class MotorMetricasHibrido:
    """Resuelve primero configuración de finca y luego catálogo oficial."""

    def __init__(self, ejecutor=None, descubridor=None):
        self.ejecutor = ejecutor or EjecutorMotorV1()
        self.descubridor = descubridor or DescubridorMetricas()

    def descubrir(self, codigo, finca=None):
        """Devuelve una definición BD si existe; si no, usa el catálogo V1."""
        try:
            return self.descubridor.descubrir(codigo, finca=finca)
        except MetricaNoDisponible:
            try:
                return obtener_metrica_v1(codigo)
            except ValueError as exc:
                raise MetricaNoEncontrada(str(exc)) from exc

    def ejecutar(self, codigo, datos, finca=None, contexto=None):
        """Descubre y ejecuta una métrica sin que el llamador conozca su origen."""
        definicion = self.descubrir(codigo, finca=finca)
        resultado = self.ejecutor.ejecutar(
            definicion,
            datos,
            contexto=contexto,
        )
        return resultado


def ejecutar_metrica(codigo, datos, finca=None, contexto=None):
    """API funcional mínima para ejecutar una métrica híbrida."""
    return MotorMetricasHibrido().ejecutar(
        codigo,
        datos,
        finca=finca,
        contexto=contexto,
    )

"""Descubrimiento de métricas configuradas en base de datos para el Motor V1.

M04 establece el puente entre la configuración persistida (Metrica) y el
contrato inmutable que consume EjecutorMotorV1 (DefinicionMetrica).
"""

from apps.produccion.engine.definicion import DefinicionMetrica
from apps.produccion.models import Metrica


class MetricaNoDisponible(Exception):
    """La métrica solicitada no existe o no está activa."""


class DescubridorMetricas:
    """Localiza una métrica persistida y la traduce al contrato del motor."""

    def descubrir(self, codigo: str, finca=None) -> DefinicionMetrica:
        consulta = Metrica.objects.filter(codigo=codigo, activa=True)
        if finca is not None:
            consulta = consulta.filter(finca=finca)

        metrica = consulta.prefetch_related("variables").first()
        if metrica is None:
            raise MetricaNoDisponible(
                f"No existe una métrica activa con código '{codigo}' "
                f"para el contexto solicitado."
            )

        variables = list(metrica.variables.filter(activa=True).order_by("orden", "codigo"))
        dependencias = [variable.codigo for variable in variables if variable.tipo == "calculada"]

        estrategia = {
            "modo": "formula" if metrica.formula.strip() else "pipeline",
            "dependencias": dependencias,
        }
        if metrica.formula.strip():
            estrategia["formula"] = metrica.formula.strip()

        return DefinicionMetrica(
            codigo=metrica.codigo,
            nombre=metrica.nombre,
            version=str(metrica.version),
            tipo="derivada" if metrica.formula.strip() else "atomica",
            familia=metrica.categoria,
            unidad=metrica.unidad_resultado,
            precision_decimales=2,
            estrategia=estrategia,
            descripcion=metrica.descripcion,
        )


def descubrir_metrica(codigo: str, finca=None) -> DefinicionMetrica:
    """Atajo público para descubrir una métrica configurable."""
    return DescubridorMetricas().descubrir(codigo, finca=finca)

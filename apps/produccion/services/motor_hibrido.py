"""Fachada de ejecución híbrida para el Motor de Métricas.

M05 unifica las fuentes de definiciones. M06 añade una frontera explícita
de seguridad para que la ejecución configurable respete tenant, usuario,
fuente de datos y lenguaje matemático permitido.
"""

from apps.produccion.engine.catalogo_v1 import obtener_metrica_v1
from apps.produccion.engine.ejecutor import EjecutorMotorV1
from apps.produccion.models import Metrica
from apps.produccion.services.descubrimiento import (
    DescubridorMetricas,
    MetricaNoDisponible,
)
from apps.produccion.services.seguridad_metricas import (
    validar_metrica_configurable,
    verificar_ejecucion_segura,
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
        """API interna de ejecución; no sustituye la frontera segura."""
        definicion = self.descubrir(codigo, finca=finca)
        return self.ejecutor.ejecutar(
            definicion,
            datos,
            contexto=contexto,
        )

    def ejecutar_seguro(
        self,
        codigo,
        datos,
        user,
        finca,
        animal=None,
        contexto=None,
    ):
        """Ejecuta una métrica con autenticación y aislamiento de tenant.

        Si existe una definición configurable para la finca, se valida antes
        de ejecutarla. Si no existe, puede utilizarse la métrica oficial del
        catálogo, pero siempre dentro de una finca autorizada.
        """
        # Para evitar cualquier ambigüedad de tenant, la finca es obligatoria.
        if finca is None:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("La finca es obligatoria para ejecución segura.")

        # Valida autenticación, pertenencia de finca y coherencia del animal.
        # Para métricas configurables también valida fórmula y variables.
        metrica_bd = (
            Metrica.objects
            .filter(codigo=codigo, finca=finca, activa=True)
            .prefetch_related("variables")
            .first()
        )
        if metrica_bd is not None:
            verificar_ejecucion_segura(user, metrica_bd, animal=animal)
            validar_metrica_configurable(metrica_bd)
        else:
            # El catálogo no tiene pertenencia propia, pero los datos sí.
            verificar_ejecucion_segura(user, Metrica(finca=finca, formula="1"), animal=animal)

        return self.ejecutar(
            codigo,
            datos,
            finca=finca,
            contexto=contexto,
        )


def ejecutar_metrica(codigo, datos, finca=None, contexto=None):
    """API funcional mínima para ejecución interna no autenticada."""
    return MotorMetricasHibrido().ejecutar(
        codigo,
        datos,
        finca=finca,
        contexto=contexto,
    )


def ejecutar_metrica_segura(
    codigo,
    datos,
    user,
    finca,
    animal=None,
    contexto=None,
):
    """API pública recomendada para ejecutar métricas desde una vista/API."""
    return MotorMetricasHibrido().ejecutar_seguro(
        codigo,
        datos,
        user=user,
        finca=finca,
        animal=animal,
        contexto=contexto,
    )

"""Boundary de seguridad para métricas híbridas.

M06 evita que una definición configurable pueda escapar del tenant,
leer fuentes/campos no autorizados o introducir expresiones fuera del
lenguaje matemático seguro del motor.
"""

import ast

from django.core.exceptions import PermissionDenied

from apps.core.tenant import verificar_acceso_finca
from apps.ganado.models import PesajeAnimal
from apps.produccion.models import Metrica, VariableMetrica


MAX_FORMULA_LENGTH = 500
MAX_VARIABLES = 50

# El motor de variables soporta actualmente esta única fuente. La lista es
# deliberadamente explícita: una métrica no puede convertir texto de BD en
# una ruta arbitraria de acceso a modelos Django.
ALLOWED_SOURCES = {
    "PesajeAnimal": frozenset(
        field.name for field in PesajeAnimal._meta.fields
        if field.name not in {"id", "animal"}
    )
}

ALLOWED_AST_NODES = (
    ast.Expression,
    ast.Constant,
    ast.Name,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Load,
)


class ConfiguracionMetricaInsegura(ValueError):
    """La definición no cumple el contrato de seguridad M06."""


def validar_formula_segura(formula: str) -> None:
    """Acepta únicamente aritmética sobre nombres y constantes."""
    if not isinstance(formula, str) or not formula.strip():
        raise ConfiguracionMetricaInsegura("La fórmula es obligatoria.")
    if len(formula) > MAX_FORMULA_LENGTH:
        raise ConfiguracionMetricaInsegura("La fórmula supera el límite permitido.")

    try:
        tree = ast.parse(formula, mode="eval")
    except SyntaxError as exc:
        raise ConfiguracionMetricaInsegura("La fórmula no es sintácticamente válida.") from exc

    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_AST_NODES):
            raise ConfiguracionMetricaInsegura(
                f"Elemento no permitido en fórmula: {type(node).__name__}."
            )
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise ConfiguracionMetricaInsegura("Solo se permiten constantes numéricas.")


def validar_variable(variable: VariableMetrica) -> None:
    """Valida fuente, campo y regla contra un catálogo explícito."""
    if variable.fuente not in ALLOWED_SOURCES:
        raise ConfiguracionMetricaInsegura(
            f"Fuente no autorizada: {variable.fuente}."
        )
    if variable.campo not in ALLOWED_SOURCES[variable.fuente]:
        raise ConfiguracionMetricaInsegura(
            f"Campo no autorizado: {variable.fuente}.{variable.campo}."
        )
    if variable.regla not in dict(VariableMetrica.REGLA_CHOICES):
        raise ConfiguracionMetricaInsegura(
            f"Regla no autorizada: {variable.regla}."
        )


def validar_metrica_configurable(metrica: Metrica) -> Metrica:
    """Valida una métrica completa antes de permitir su ejecución."""
    if metrica.finca_id is None:
        raise ConfiguracionMetricaInsegura(
            "Una métrica configurable debe pertenecer a una finca."
        )
    validar_formula_segura(metrica.formula)

    variables = list(metrica.variables.filter(activa=True).order_by("orden", "codigo"))
    if not variables:
        raise ConfiguracionMetricaInsegura("La métrica debe tener al menos una variable activa.")
    if len(variables) > MAX_VARIABLES:
        raise ConfiguracionMetricaInsegura("La métrica supera el máximo de variables permitido.")

    codigos = {variable.codigo for variable in variables}
    for variable in variables:
        validar_variable(variable)

    tree = ast.parse(metrica.formula, mode="eval")
    nombres = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    faltantes = nombres - codigos
    if faltantes:
        raise ConfiguracionMetricaInsegura(
            "La fórmula contiene variables no declaradas: " + ", ".join(sorted(faltantes))
        )

    return metrica


def verificar_ejecucion_segura(user, metrica: Metrica, animal=None) -> None:
    """Impone autenticación, pertenencia de finca y coherencia del animal."""
    if not getattr(user, "is_authenticated", False):
        raise PermissionDenied("Debe iniciar sesión para ejecutar métricas.")
    if not verificar_acceso_finca(user, metrica.finca):
        raise PermissionDenied("No tiene autorización para esta finca.")
    if animal is not None and getattr(animal, "finca_id", None) != metrica.finca_id:
        raise PermissionDenied("El animal no pertenece a la finca de la métrica.")

    validar_metrica_configurable(metrica)

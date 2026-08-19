"""Ejecutor oficial del Motor de Métricas Hato V1."""

from decimal import Decimal
from typing import Any, Dict, Optional

from .compositor import Compositor
from .evaluador import evaluar_expresion
from .definicion import DefinicionMetrica
from .resultado import ResultadoMetrica
from .excepciones import (
    ErrorCalculoMetrica, ErrorComposicion, ErrorDatosInsuficientes,
    ErrorDivisionPorCero, ErrorMotorMetrica,
)

class EjecutorMotorV1:
    def __init__(self) -> None:
        self.compositor = Compositor()

    def ejecutar(self, definicion: DefinicionMetrica, datos: Any,
                 contexto: Optional[Dict[str, Any]] = None) -> ResultadoMetrica:
        ctx = contexto or {}
        modo = definicion.estrategia.get("modo", "pipeline")
        try:
            if modo == "pipeline":
                return self._ejecutar_pipeline(definicion, datos, ctx)
            if modo == "formula":
                return self._ejecutar_formula(definicion, datos, ctx)
            raise ErrorCalculoMetrica(f"Modo de estrategia no soportado: {modo}")
        except ErrorMotorMetrica as err:
            return ResultadoMetrica(definicion.codigo, definicion.nombre, None,
                                    definicion.unidad, False, error=str(err))
        except ZeroDivisionError as err:
            return ResultadoMetrica(definicion.codigo, definicion.nombre, None,
                                    definicion.unidad, False,
                                    error=f"Error de división por cero: {err}")
        except Exception as err:
            return ResultadoMetrica(definicion.codigo, definicion.nombre, None,
                                    definicion.unidad, False,
                                    error=f"Error inesperado durante la ejecución: {err}")

    def _ejecutar_pipeline(self, definicion, datos, contexto):
        pasos = [dict(p) for p in definicion.pasos]
        if "sexo" in contexto:
            for paso in pasos:
                if (paso.get("funcion") == "FILTRO" and
                    paso.get("parametros", {}).get("campo") == "sexo"):
                    paso["parametros"] = {"campo":"sexo", "valor":contexto["sexo"]}
        validacion = self.compositor.validar(pasos)
        if not validacion.get("valido", False):
            raise ErrorComposicion(f"Validación de pipeline fallida para {definicion.codigo}")
        explicacion = self.compositor.explicar(pasos)
        entrada = datos
        if hasattr(datos, "all") and callable(getattr(datos, "all")):
            entrada = list(datos.all())
        elif hasattr(datos, "__iter__") and not isinstance(datos, (str, bytes, dict)):
            entrada = list(datos)
        valor_crudo = self.compositor.ejecutar(entrada, pasos)
        valor_final = self._formatear_valor(valor_crudo, definicion.precision_decimales)
        return ResultadoMetrica(
            definicion.codigo, definicion.nombre, valor_final, definicion.unidad, True,
            definicion.precision_decimales,
            {"pasos_ejecutados":explicacion.get("pasos", []),
             "tipo_salida":explicacion.get("salida"),
             "elementos_recibidos":len(entrada) if isinstance(entrada, list) else 1},
        )

    def _ejecutar_formula(self, definicion, datos, contexto):
        formula = definicion.formula
        if not formula:
            raise ErrorCalculoMetrica(f"La métrica derivada {definicion.codigo} no define fórmula.")
        if not isinstance(datos, dict):
            raise ErrorCalculoMetrica("Las métricas derivadas requieren un diccionario de variables como entrada.")
        variables = {}
        for k, v in datos.items():
            if v is None:
                raise ErrorDatosInsuficientes(f"La variable '{k}' es requerida y tiene valor nulo.")
            variables[k] = Decimal(str(v))
        if "hectareas" in variables and variables["hectareas"] <= Decimal("0"):
            raise ErrorDivisionPorCero("El área en hectáreas no puede ser menor o igual a cero.")
        valor_final = self._formatear_valor(evaluar_expresion(formula, variables), definicion.precision_decimales)
        return ResultadoMetrica(
            definicion.codigo, definicion.nombre, valor_final, definicion.unidad, True,
            definicion.precision_decimales,
            {"formula":formula, "variables":{k:str(v) for k,v in variables.items()},
             "dependencias":definicion.dependencias},
        )

    def _formatear_valor(self, valor, precision):
        if isinstance(valor, (int, float, Decimal, str)):
            try:
                dec = Decimal(str(valor))
                if precision == 0:
                    return int(dec)
                return round(dec, precision)
            except Exception:
                return valor
        return valor

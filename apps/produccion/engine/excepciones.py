"""Excepciones tipadas para el Motor de Métricas Hato V1."""

class ErrorMotorMetrica(Exception):
    """Excepción base para todos los errores del motor de métricas."""
    pass

class ErrorComposicion(ErrorMotorMetrica):
    """Error cuando la composición de pasos es inválida o incompatible."""
    pass

class ErrorCalculoMetrica(ErrorMotorMetrica):
    """Error durante la ejecución matemática o lógica de una métrica."""
    pass

class ErrorDatosInsuficientes(ErrorCalculoMetrica):
    """Error cuando los datos fuente no alcanzan el mínimo requerido."""
    pass

class ErrorDivisionPorCero(ErrorCalculoMetrica):
    """Error cuando el denominador de una tasa o ratio no es válido."""
    pass

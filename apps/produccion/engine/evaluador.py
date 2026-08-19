from decimal import Decimal
import ast
import operator

OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def evaluar_expresion(expresion: str, variables: dict) -> Decimal:
    """Evalúa una fórmula matemática segura mediante AST y Decimal."""
    arbol = ast.parse(expresion, mode="eval")
    def evaluar(nodo):
        if isinstance(nodo, ast.Expression): return evaluar(nodo.body)
        if isinstance(nodo, ast.Constant): return Decimal(str(nodo.value))
        if isinstance(nodo, ast.Name):
            if nodo.id not in variables: raise ValueError(f"Variable no definida: {nodo.id}")
            valor=variables[nodo.id]
            if valor is None: raise ValueError(f"La variable {nodo.id} no tiene valor.")
            return Decimal(str(valor))
        if isinstance(nodo, ast.BinOp):
            operador=OPERADORES.get(type(nodo.op))
            if operador is None: raise ValueError(f"Operador no permitido: {type(nodo.op).__name__}")
            return operador(evaluar(nodo.left), evaluar(nodo.right))
        if isinstance(nodo, ast.UnaryOp):
            operador=OPERADORES.get(type(nodo.op))
            if operador is None: raise ValueError(f"Operador no permitido: {type(nodo.op).__name__}")
            return operador(evaluar(nodo.operand))
        raise ValueError(f"Expresión no permitida: {type(nodo).__name__}")
    return evaluar(arbol)

def evaluar_metrica(metrica, objeto):
    from .variables import resolver_variable
    if not metrica.activa: raise ValueError(f"La métrica {metrica.codigo} está inactiva.")
    if not metrica.formula: raise ValueError(f"La métrica {metrica.codigo} no tiene fórmula.")
    variables={}
    for variable in metrica.variables.filter(activa=True).order_by("orden"):
        variables[variable.codigo]=resolver_variable(variable,objeto)
    resultado=evaluar_expresion(metrica.formula,variables)
    return {"metrica":metrica.codigo,"nombre":metrica.nombre,"formula":metrica.formula,
            "variables":variables,"resultado":resultado,"unidad":metrica.unidad_resultado,
            "tipo_resultado":metrica.tipo_resultado}

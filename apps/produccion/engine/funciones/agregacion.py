from decimal import Decimal
from .base import FuncionBase
from apps.produccion.engine.excepciones import ErrorDatosInsuficientes

class Conteo(FuncionBase):
    codigo="CONTEO"; nombre="Conteo"; unidad="elementos"; entrada="elementos|valores"; salida="valor"
    def ejecutar(self, contexto):
        valores=contexto.get("valores")
        if valores is not None: return len([v for v in valores if v is not None])
        elementos=contexto.get("elementos")
        if elementos is not None: return len(elementos)
        return 0

class Suma(FuncionBase):
    codigo="SUMA"; nombre="Suma"; unidad=None; entrada="elementos|valores"; salida="valor"
    def ejecutar(self, contexto):
        valores=contexto.get("valores")
        if valores is None:
            elementos=contexto.get("elementos")
            funcion=contexto.get("funcion")
            if elementos is not None:
                if funcion is not None:
                    if isinstance(funcion,str):
                        from . import obtener_funcion
                        funcion=obtener_funcion(funcion)
                    valores=[]
                    for elem in elementos:
                        val=funcion.ejecutar({"animal":elem,"elemento":elem})
                        if val is not None: valores.append(val)
                else: valores=elementos
        if not valores: return Decimal("0.00")
        total=Decimal("0.00")
        for v in valores:
            if v is not None: total += Decimal(str(v))
        return total

class Promedio(FuncionBase):
    codigo="PROMEDIO"; nombre="Promedio"; unidad=None; entrada="elementos|valores"; salida="valor"
    def ejecutar(self, contexto):
        valores=contexto.get("valores")
        if valores is None:
            elementos=contexto.get("elementos")
            funcion=contexto.get("funcion")
            if elementos is not None:
                if funcion is not None:
                    if isinstance(funcion,str):
                        from . import obtener_funcion
                        funcion=obtener_funcion(funcion)
                    valores=[]
                    for elem in elementos:
                        val=funcion.ejecutar({"animal":elem,"elemento":elem})
                        if val is not None: valores.append(val)
                else: valores=elementos
        if not valores: raise ErrorDatosInsuficientes("No existen valores para calcular el promedio.")
        valores_validos=[Decimal(str(v)) for v in valores if v is not None]
        if not valores_validos: raise ErrorDatosInsuficientes("No existen valores válidos para calcular el promedio.")
        return round(sum(valores_validos)/Decimal(str(len(valores_validos))),2)

class Filtro(FuncionBase):
    codigo="FILTRO"; nombre="Filtro"; unidad="elementos"; entrada="elementos"; salida="elementos"
    def ejecutar(self, contexto):
        elementos=contexto.get("elementos")
        if elementos is None: return []
        campo=contexto.get("campo")
        if not campo: raise ValueError("FILTRO requiere el parámetro 'campo'.")
        valor=contexto.get("valor")
        resultado=[]
        for elemento in elementos:
            if hasattr(elemento,campo): valor_elemento=getattr(elemento,campo)
            elif isinstance(elemento,dict) and campo in elemento: valor_elemento=elemento[campo]
            else: raise ValueError(f"El campo '{campo}' no existe en el elemento.")
            if valor_elemento==valor: resultado.append(elemento)
        return resultado

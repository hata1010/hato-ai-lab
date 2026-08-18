from .base import FuncionBase


class Mapear(FuncionBase):

    codigo = "MAPEAR"
    nombre = "Mapear"
    unidad = None
    
    entrada = "elementos"
    salida = "valores"

    def ejecutar(self, contexto):

        elementos = contexto.get("elementos")
        funcion = contexto.get("funcion")

        if elementos is None:
            raise ValueError(
                "MAPEAR necesita una colección de elementos."
            )

        if funcion is None:
            raise ValueError(
                "MAPEAR necesita una función."
            )

        # ------------------------------------------------
        # Permitir código o instancia de función
        # ------------------------------------------------

        if isinstance(funcion, str):

            from . import obtener_funcion

            funcion = obtener_funcion(funcion)

        # ------------------------------------------------
        # Ejecutar la función sobre cada elemento
        # ------------------------------------------------

        resultados = []

        for elemento in elementos:

            resultado = funcion.ejecutar({
                "animal": elemento
            })

            if resultado is not None:
                resultados.append(resultado)

        return resultados
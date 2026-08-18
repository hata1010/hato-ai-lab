from .base import FuncionBase


class Promedio(FuncionBase):

    codigo = "PROMEDIO"
    nombre = "Promedio"
    unidad = None
    entrada = "valores"
    salida = "valor"

    def ejecutar(self, contexto):

        # ----------------------------------------------------
        # MODO 1: recibir valores directamente
        # ----------------------------------------------------

        valores = contexto.get("valores")

        if valores is not None:

            valores = [
                valor
                for valor in valores
                if valor is not None
            ]

            if not valores:
                raise ValueError(
                    "No existen valores para calcular el promedio."
                )

            return sum(valores) / len(valores)

        # ----------------------------------------------------
        # MODO 2: recibir elementos + función
        # ----------------------------------------------------

        elementos = contexto.get("elementos")
        funcion = contexto.get("funcion")

        if elementos is None:
            raise ValueError(
                "PROMEDIO requiere 'valores' "
                "o 'elementos'."
            )

        if funcion is None:
            raise ValueError(
                "PROMEDIO requiere una 'funcion' "
                "cuando recibe elementos."
            )

        valores = []

        for elemento in elementos:

            valor = funcion.ejecutar({
                "animal": elemento,
            })

            if valor is not None:
                valores.append(valor)

        if not valores:
            raise ValueError(
                "La función no produjo valores."
            )

        return sum(valores) / len(valores)
    
class Suma(FuncionBase):

    codigo = "SUMA"
    nombre = "Suma"
    unidad = None
    entrada = "valores"
    salida = "valor"

    def ejecutar(self, contexto):

        # ----------------------------------------------------
        # MODO 1: recibir valores directamente
        # ----------------------------------------------------

        valores = contexto.get("valores")

        if valores is not None:

            valores = [
                valor
                for valor in valores
                if valor is not None
            ]

            if not valores:
                raise ValueError(
                    "No existen valores para sumar."
                )

            return sum(valores)

        # ----------------------------------------------------
        # MODO 2: recibir elementos + función
        # ----------------------------------------------------

        elementos = contexto.get("elementos")
        funcion = contexto.get("funcion")

        if elementos is None:
            raise ValueError(
                "SUMA requiere 'valores' "
                "o 'elementos'."
            )

        if funcion is None:
            raise ValueError(
                "SUMA requiere una 'funcion' "
                "cuando recibe elementos."
            )

        valores = []

        for elemento in elementos:

            valor = funcion.ejecutar({
                "animal": elemento,
            })

            if valor is not None:
                valores.append(valor)

        if not valores:
            raise ValueError(
                "La función no produjo valores."
            )

        return sum(valores)
    
class Conteo(FuncionBase):

    codigo = "CONTEO"
    nombre = "Conteo"
    unidad = "elementos"
    entrada = "elementos|valores"
    salida = "valor"

    def ejecutar(self, contexto):

        # ----------------------------------------------------
        # MODO 1: recibir valores directamente
        # ----------------------------------------------------

        valores = contexto.get("valores")

        if valores is not None:

            valores = [
                valor
                for valor in valores
                if valor is not None
            ]

            return len(valores)

        # ----------------------------------------------------
        # MODO 2: recibir elementos
        # ----------------------------------------------------

        elementos = contexto.get("elementos")

        if elementos is not None:
            return len(elementos)

        raise ValueError(
            "CONTEO requiere 'valores' "
            "o 'elementos'."
        )
        
class Filtro(FuncionBase):

    codigo = "FILTRO"
    nombre = "Filtro"
    unidad = "elementos" 
    entrada = "elementos"
    salida = "elementos"

    def ejecutar(self, contexto):

        elementos = contexto.get("elementos")

        if elementos is None:
            raise ValueError(
                "FILTRO requiere 'elementos'."
            )

        campo = contexto.get("campo")

        if not campo:
            raise ValueError(
                "FILTRO requiere 'campo'."
            )

        valor = contexto.get("valor")

        resultado = []

        for elemento in elementos:

            try:
                valor_elemento = getattr(
                    elemento,
                    campo,
                )

            except AttributeError:
                raise ValueError(
                    f"El campo '{campo}' "
                    f"no existe en el elemento."
                )

            if valor_elemento == valor:
                resultado.append(elemento)

        return resultado
    

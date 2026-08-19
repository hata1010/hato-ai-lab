from apps.produccion.engine.funciones import obtener_funcion
from apps.produccion.engine.excepciones import ErrorComposicion


class Compositor:
    """Valida, explica y ejecuta pipelines de funciones compuestas."""

    def validar(self, pasos):
        tipo_actual = "elementos"
        for paso in pasos:
            codigo = paso.get("funcion")
            if not codigo:
                raise ErrorComposicion("Cada paso debe indicar una función.")
            funcion = obtener_funcion(codigo)
            entrada_requerida = funcion.entrada
            salida_producida = funcion.salida
            if entrada_requerida is None:
                raise ErrorComposicion(f"La función {codigo} no tiene entrada definida.")
            if salida_producida is None:
                raise ErrorComposicion(f"La función {codigo} no tiene salida definida.")
            entradas_validas = [e.strip() for e in entrada_requerida.split("|")]
            if tipo_actual not in entradas_validas:
                raise ErrorComposicion(
                    f"Composición inválida: {codigo} requiere '{entrada_requerida}', "
                    f"pero recibe '{tipo_actual}'."
                )
            tipo_actual = salida_producida
        return {"valido": True, "salida": tipo_actual}

    def explicar(self, pasos):
        explicacion = []
        tipo_actual = "elementos"
        for numero, paso in enumerate(pasos, start=1):
            codigo = paso.get("funcion")
            if not codigo:
                raise ErrorComposicion("Cada paso debe indicar una función.")
            funcion = obtener_funcion(codigo)
            parametros = paso.get("parametros", {})
            explicacion.append({
                "paso": numero,
                "funcion": codigo,
                "entrada": funcion.entrada,
                "salida": funcion.salida,
                "parametros": parametros,
            })
            tipo_actual = funcion.salida
        return {"valido": True, "pasos": explicacion, "salida": tipo_actual}

    def ejecutar(self, entrada, pasos):
        resultado = entrada
        for paso in pasos:
            codigo = paso.get("funcion")
            if not codigo:
                raise ErrorComposicion("Cada paso debe indicar una función.")
            funcion = obtener_funcion(codigo)
            parametros = paso.get("parametros", {})
            entrada_tipo = paso.get("entrada")
            if entrada_tipo is None:
                contrato = funcion.entrada
                if contrato is None or "|" in contrato:
                    entrada_tipo = "elementos"
                else:
                    entrada_tipo = contrato
            contexto = {entrada_tipo: resultado, **parametros}
            resultado = funcion.ejecutar(contexto)
        return resultado

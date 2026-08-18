from apps.produccion.engine.funciones import obtener_funcion


class ErrorComposicion(Exception):
    pass


class Compositor:

    def validar(self, pasos):

        tipo_actual = "elementos"

        for paso in pasos:

            codigo = paso.get("funcion")

            if not codigo:
                raise ErrorComposicion(
                    "Cada paso debe indicar una función."
                )

            funcion = obtener_funcion(codigo)

            entrada_requerida = funcion.entrada
            salida_producida = funcion.salida

            if entrada_requerida is None:
                raise ErrorComposicion(
                    f"La función {codigo} "
                    "no tiene entrada definida."
                )

            if salida_producida is None:
                raise ErrorComposicion(
                    f"La función {codigo} "
                    "no tiene salida definida."
                )

            entradas_validas = [
                entrada.strip()
                for entrada in entrada_requerida.split("|")
            ]

            if tipo_actual not in entradas_validas:
                raise ErrorComposicion(
                    f"Composición inválida: "
                    f"{codigo} requiere "
                    f"'{entrada_requerida}', "
                    f"pero recibe '{tipo_actual}'."
                )

            tipo_actual = salida_producida

        return {
            "valido": True,
            "salida": tipo_actual,
        }

    def explicar(self, pasos):

        explicacion = []

        tipo_actual = "elementos"

        for numero, paso in enumerate(pasos, start=1):

            codigo = paso.get("funcion")

            if not codigo:
                raise ErrorComposicion(
                    "Cada paso debe indicar una función."
                )

            funcion = obtener_funcion(codigo)

            entrada = funcion.entrada
            salida = funcion.salida

            parametros = paso.get(
                "parametros",
                {}
            )

            explicacion.append({
                "paso": numero,
                "funcion": codigo,
                "entrada": entrada,
                "salida": salida,
                "parametros": parametros,
            })

            tipo_actual = salida

        return {
            "valido": True,
            "pasos": explicacion,
            "salida": tipo_actual,
        }

    def ejecutar(self, entrada, pasos):

        resultado = entrada

        for paso in pasos:

            codigo = paso.get("funcion")

            if not codigo:
                raise ErrorComposicion(
                    "Cada paso debe indicar una función."
                )

            funcion = obtener_funcion(codigo)

            parametros = paso.get(
                "parametros",
                {}
            )

            # -----------------------------------------
            # Determinar automáticamente la entrada
            # -----------------------------------------

            entrada_tipo = paso.get("entrada")

            if entrada_tipo is None:

                contrato = funcion.entrada

                if contrato is None:
                    entrada_tipo = "elementos"

                elif "|" in contrato:
                    entrada_tipo = "elementos"

                else:
                    entrada_tipo = contrato

            # -----------------------------------------
            # Construir contexto
            # -----------------------------------------

            contexto = {
                entrada_tipo: resultado,
                **parametros,
            }

            # -----------------------------------------
            # Ejecutar función
            # -----------------------------------------

            resultado = funcion.ejecutar(
                contexto
            )

        return resultado
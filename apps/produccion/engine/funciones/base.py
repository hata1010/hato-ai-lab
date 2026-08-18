class FuncionBase:
    """
    Clase base para todas las funciones del catálogo Hato.

    Una función representa una operación reutilizable
    que puede ser invocada por el motor.
    """

    codigo = None
    nombre = None
    unidad = None

    # ----------------------------------------------------
    # CONTRATO DE DATOS
    # ----------------------------------------------------

    entrada = None
    salida = None

    # ----------------------------------------------------
    # EJECUCIÓN
    # ----------------------------------------------------

    def ejecutar(self, contexto):
        """
        Ejecuta la función utilizando el contexto recibido.

        Las funciones hijas deben implementar este método.
        """

        raise NotImplementedError(
            f"La función {self.codigo} "
            "no implementa el método ejecutar()."
        )
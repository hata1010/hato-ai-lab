from apps.produccion.engine.compositor import Compositor


class PlanMetrica:
    """
    Define una métrica como una secuencia de funciones
    que el motor puede validar, explicar y ejecutar.
    """

    def __init__(self, nombre, pasos):
        self.nombre = nombre
        self.pasos = pasos
        self.compositor = Compositor()

    # --------------------------------------------------
    # VALIDAR
    # --------------------------------------------------

    def validar(self):

        resultado = self.compositor.validar(
            self.pasos
        )

        return resultado

    # --------------------------------------------------
    # EXPLICAR
    # --------------------------------------------------

    def explicar(self):

        return self.compositor.explicar(
            self.pasos
        )

    # --------------------------------------------------
    # EJECUTAR
    # --------------------------------------------------

    def ejecutar(self, entrada):

        return self.compositor.ejecutar(
            entrada,
            self.pasos
        )

    # --------------------------------------------------
    # INFORMACIÓN GENERAL
    # --------------------------------------------------

    def informacion(self):

        validacion = self.validar()

        return {
            "nombre": self.nombre,
            "valido": validacion["valido"],
            "salida": validacion["salida"],
            "pasos": self.pasos,
        }

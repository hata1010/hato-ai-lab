class Metrica:

    def __init__(
        self,
        codigo,
        nombre,
        pasos,
        unidad=None,
        descripcion=None,
    ):
        self.codigo = codigo
        self.nombre = nombre
        self.pasos = pasos
        self.unidad = unidad
        self.descripcion = descripcion

    def ejecutar(self, entrada):

        from apps.produccion.engine.compositor import Compositor

        compositor = Compositor()

        return compositor.ejecutar(
            entrada,
            self.pasos,
        )

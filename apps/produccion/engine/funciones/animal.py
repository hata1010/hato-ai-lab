from apps.produccion.engine.funciones.base import FuncionBase
from apps.ganado.models import PesajeAnimal


class PesoActual(FuncionBase):
    """
    Devuelve el último peso registrado de un animal. metadatos
    """

    codigo = "PESO_ACTUAL"
    nombre = "Peso actual"
    unidad = "kg"
    entrada = "elemento"
    salida = "valor"

    def ejecutar(self, contexto):
        animal = contexto.get("animal")

        if animal is None:
            raise ValueError(
                "PESO_ACTUAL requiere un animal."
            )

        pesaje = (
            PesajeAnimal.objects
            .filter(animal=animal)
            .order_by("-fecha")
            .first()
        )

        if pesaje is None:
            raise ValueError(
                f"El animal {animal.numero_arete} "
                "no tiene pesajes registrados."
            )

        return pesaje.peso_kg
    


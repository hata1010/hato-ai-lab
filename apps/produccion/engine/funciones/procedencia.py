from .base import FuncionBase
from apps.ganado.models import ProcedenciaAnimal


class FiltroProcedencia(FuncionBase):
    """Filtra animales por el tipo de procedencia registrado."""

    codigo = "FILTRO_PROCEDENCIA"
    nombre = "Filtro por procedencia"
    unidad = "elementos"
    entrada = "elementos"
    salida = "elementos"

    def ejecutar(self, contexto):
        elementos = contexto.get("elementos")
        if elementos is None:
            return []

        valor = contexto.get("valor")
        if not valor:
            raise ValueError("FILTRO_PROCEDENCIA requiere el parámetro 'valor'.")

        resultado = []
        for animal in elementos:
            animal_id = getattr(animal, "id", None)
            if animal_id is None:
                continue
            if ProcedenciaAnimal.objects.filter(
                animal_id=animal_id,
                tipo=valor,
            ).exists():
                resultado.append(animal)
        return resultado

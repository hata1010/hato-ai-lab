from datetime import datetime
from decimal import Decimal

from .base import FuncionBase
from .excepciones import ErrorDatosInsuficientes, ErrorDivisionPorCero


class IntervaloEntrePartos(FuncionBase):
    codigo = "IEP_ANIMAL"
    nombre = "Intervalo entre partos"
    unidad = "dias"
    entrada = "animal"
    salida = "valor"

    def ejecutar(self, contexto):
        animal = contexto.get("animal")
        if animal is None:
            raise ValueError("IEP_ANIMAL requiere un animal en el contexto.")

        eventos = list(
            animal.eventos_reproductivos.filter(tipo_evento="parto")
            .order_by("-fecha")[:2]
        )
        if len(eventos) < 2:
            raise ErrorDatosInsuficientes(
                "Se requieren al menos 2 partos válidos para calcular el intervalo entre partos."
            )

        reciente, anterior = eventos[0].fecha, eventos[1].fecha
        dias = (reciente.date() - anterior.date()).days
        if dias <= 0:
            raise ErrorDivisionPorCero("Las fechas de parto no forman un intervalo válido.")
        return dias


class DiasAbiertos(FuncionBase):
    codigo = "DIAS_ABIERTOS_ANIMAL"
    nombre = "Días abiertos"
    unidad = "dias"
    entrada = "animal"
    salida = "valor"

    def ejecutar(self, contexto):
        animal = contexto.get("animal")
        if animal is None:
            raise ValueError("DIAS_ABIERTOS_ANIMAL requiere un animal en el contexto.")

        ultimo_parto = (
            animal.eventos_reproductivos.filter(tipo_evento="parto")
            .order_by("-fecha")
            .first()
        )
        if ultimo_parto is None:
            raise ErrorDatosInsuficientes(
                "Se requiere un parto registrado para calcular días abiertos."
            )

        concepcion = (
            animal.eventos_reproductivos.filter(
                tipo_evento="diagnostico_gestacion",
                resultado_gestacion="prenada",
                fecha__gt=ultimo_parto.fecha,
            )
            .order_by("fecha")
            .first()
        )
        if concepcion is None:
            raise ErrorDatosInsuficientes(
                "No existe un diagnóstico de gestación positivo posterior al último parto."
            )

        dias = (concepcion.fecha.date() - ultimo_parto.fecha.date()).days
        if dias <= 0:
            raise ErrorDivisionPorCero("El diagnóstico positivo no forma un intervalo válido con el parto.")
        return dias


class ProduccionAcumuladaLactancia(FuncionBase):
    codigo = "LECHE_ACUM_LACTANCIA"
    nombre = "Producción acumulada de lactancia"
    unidad = "unidad_control"
    entrada = "lactancia"
    salida = "valor"

    def ejecutar(self, contexto):
        lactancia = contexto.get("lactancia")
        if lactancia is None:
            raise ValueError("LECHE_ACUM_LACTANCIA requiere una lactancia en el contexto.")

        controles = list(lactancia.controles_leche.order_by("fecha"))
        if not controles:
            raise ErrorDatosInsuficientes(
                "Se requiere al menos un control de leche para calcular producción acumulada."
            )

        unidades = {control.unidad for control in controles}
        if len(unidades) != 1:
            raise ErrorDatosInsuficientes(
                "No se puede acumular una serie de leche con unidades mezcladas sin una conversión explícita."
            )

        return sum((Decimal(str(control.cantidad)) for control in controles), Decimal("0"))


class DuracionLactancia(FuncionBase):
    codigo = "DURACION_LACTANCIA"
    nombre = "Duración de lactancia"
    unidad = "dias"
    entrada = "lactancia"
    salida = "valor"

    def ejecutar(self, contexto):
        lactancia = contexto.get("lactancia")
        if lactancia is None:
            raise ValueError("DURACION_LACTANCIA requiere una lactancia en el contexto.")
        if lactancia.fecha_secado is None:
            raise ErrorDatosInsuficientes(
                "La lactancia aún no tiene fecha de secado; la duración final no está determinada."
            )
        dias = (lactancia.fecha_secado - lactancia.fecha_inicio).days
        if dias < 0:
            raise ErrorDivisionPorCero("La fecha de secado no puede ser anterior al inicio de la lactancia.")
        return dias

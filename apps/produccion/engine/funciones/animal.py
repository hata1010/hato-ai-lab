from decimal import Decimal
from datetime import datetime
from .base import FuncionBase
from apps.produccion.engine.evaluador import evaluar_expresion
from apps.produccion.engine.excepciones import ErrorDatosInsuficientes, ErrorDivisionPorCero

class PesoActual(FuncionBase):
    codigo = "PESO_ACTUAL"
    nombre = "Peso actual"
    unidad = "kg"
    entrada = "elemento|elementos"
    salida = "valor"

    def ejecutar(self, contexto):
        animal = contexto.get("animal") or contexto.get("elemento") or contexto.get("elementos")
        if animal is None:
            raise ValueError("PESO_ACTUAL requiere un animal en el contexto.")
        if hasattr(animal, "pesajes"):
            pesaje = animal.pesajes.order_by("-fecha").first()
            if pesaje is None:
                return None
            return Decimal(str(pesaje.peso_kg))
        if hasattr(animal, "peso_actual") and getattr(animal, "peso_actual") is not None:
            return Decimal(str(getattr(animal, "peso_actual")))
        return None

class GananciaMediaDiaria(FuncionBase):
    codigo = "GMD_ANIMAL"
    nombre = "Ganancia media diaria"
    unidad = "kg/dia"
    entrada = "elemento|elementos"
    salida = "valor"

    def ejecutar(self, contexto):
        animal = contexto.get("animal") or contexto.get("elemento") or contexto.get("elementos")
        if animal is None:
            raise ValueError("GMD_ANIMAL requiere un animal en el contexto.")
        if hasattr(animal, "pesajes"):
            pesajes_raw = list(animal.pesajes.order_by("-fecha")[:2])
        elif hasattr(animal, "lista_pesajes"):
            pesajes_raw = sorted(animal.lista_pesajes, key=lambda p: p["fecha"], reverse=True)[:2]
        else:
            pesajes_raw = []
        if len(pesajes_raw) < 2:
            arete = getattr(animal, "numero_arete", str(animal))
            raise ErrorDatosInsuficientes(f"El animal {arete} requiere al menos 2 pesajes para calcular GMD.")
        reciente, anterior = pesajes_raw[0], pesajes_raw[1]
        f_rec = reciente.fecha if hasattr(reciente, "fecha") else reciente["fecha"]
        f_ant = anterior.fecha if hasattr(anterior, "fecha") else anterior["fecha"]
        d_rec = f_rec.date() if isinstance(f_rec, datetime) else f_rec
        d_ant = f_ant.date() if isinstance(f_ant, datetime) else f_ant
        dias = (d_rec - d_ant).days
        if dias <= 0:
            arete = getattr(animal, "numero_arete", str(animal))
            raise ErrorDivisionPorCero(f"Intervalo de fechas inválido ({dias} días) para calcular GMD en {arete}.")
        p_rec = reciente.peso_kg if hasattr(reciente, "peso_kg") else reciente["peso_kg"]
        p_ant = anterior.peso_kg if hasattr(anterior, "peso_kg") else anterior["peso_kg"]
        variables = {"peso_final": Decimal(str(p_rec)), "peso_inicial": Decimal(str(p_ant)), "dias": Decimal(str(dias))}
        return round(evaluar_expresion("(peso_final - peso_inicial) / dias", variables), 3)

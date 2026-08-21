from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.produccion.engine.excepciones import ErrorDatosInsuficientes
from apps.produccion.engine.funciones import obtener_funcion


class ManagerStub:
    def __init__(self, items):
        self.items = list(items)

    def filter(self, **kwargs):
        result = self.items
        for key, expected in kwargs.items():
            if "__" in key:
                field, lookup = key.split("__", 1)
                if lookup == "gt":
                    result = [item for item in result if getattr(item, field) > expected]
                else:
                    raise AssertionError(f"Lookup no soportado en stub: {lookup}")
            else:
                result = [item for item in result if getattr(item, key) == expected]
        return ManagerStub(result)

    def order_by(self, field):
        reverse = field.startswith("-")
        field = field.lstrip("-")
        return ManagerStub(sorted(self.items, key=lambda item: getattr(item, field), reverse=reverse))

    def first(self):
        return self.items[0] if self.items else None

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)


class ReproduccionLactanciaMetricasTests(SimpleTestCase):
    def test_funciones_estan_registradas(self):
        for codigo in (
            "IEP_ANIMAL",
            "DIAS_ABIERTOS_ANIMAL",
            "LECHE_ACUM_LACTANCIA",
            "DURACION_LACTANCIA",
        ):
            self.assertIsNotNone(obtener_funcion(codigo))

    def test_intervalo_entre_partos(self):
        eventos = [
            SimpleNamespace(tipo_evento="parto", fecha=datetime(2026, 8, 1)),
            SimpleNamespace(tipo_evento="parto", fecha=datetime(2025, 7, 27)),
        ]
        animal = SimpleNamespace(eventos_reproductivos=ManagerStub(eventos))
        self.assertEqual(obtener_funcion("IEP_ANIMAL").ejecutar({"animal": animal}), 370)

    def test_dias_abiertos_usa_diagnostico_positivo_posterior_al_parto(self):
        eventos = [
            SimpleNamespace(tipo_evento="parto", resultado_gestacion=None, fecha=datetime(2026, 1, 1)),
            SimpleNamespace(tipo_evento="diagnostico_gestacion", resultado_gestacion="vacia", fecha=datetime(2026, 3, 1)),
            SimpleNamespace(tipo_evento="diagnostico_gestacion", resultado_gestacion="prenada", fecha=datetime(2026, 4, 1)),
        ]
        animal = SimpleNamespace(eventos_reproductivos=ManagerStub(eventos))
        self.assertEqual(obtener_funcion("DIAS_ABIERTOS_ANIMAL").ejecutar({"animal": animal}), 90)

    def test_produccion_acumulada_rechaza_unidades_mezcladas(self):
        controles = [
            SimpleNamespace(cantidad=Decimal("10.5"), unidad="l", fecha=datetime(2026, 8, 1)),
            SimpleNamespace(cantidad=Decimal("9.5"), unidad="kg", fecha=datetime(2026, 8, 2)),
        ]
        lactancia = SimpleNamespace(controles_leche=ManagerStub(controles))
        with self.assertRaises(ErrorDatosInsuficientes):
            obtener_funcion("LECHE_ACUM_LACTANCIA").ejecutar({"lactancia": lactancia})

    def test_produccion_acumulada_mantiene_unidad_homogenea(self):
        controles = [
            SimpleNamespace(cantidad=Decimal("10.5"), unidad="l", fecha=datetime(2026, 8, 1)),
            SimpleNamespace(cantidad=Decimal("9.5"), unidad="l", fecha=datetime(2026, 8, 2)),
        ]
        lactancia = SimpleNamespace(controles_leche=ManagerStub(controles))
        self.assertEqual(
            obtener_funcion("LECHE_ACUM_LACTANCIA").ejecutar({"lactancia": lactancia}),
            Decimal("20.0"),
        )

    def test_duracion_lactancia_requiere_secado(self):
        lactancia = SimpleNamespace(fecha_inicio=date(2026, 1, 1), fecha_secado=None)
        with self.assertRaises(ErrorDatosInsuficientes):
            obtener_funcion("DURACION_LACTANCIA").ejecutar({"lactancia": lactancia})

    def test_duracion_lactancia_cerrada(self):
        lactancia = SimpleNamespace(fecha_inicio=date(2026, 1, 1), fecha_secado=date(2026, 4, 1))
        self.assertEqual(obtener_funcion("DURACION_LACTANCIA").ejecutar({"lactancia": lactancia}), 90)

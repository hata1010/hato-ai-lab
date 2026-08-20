from django.test import TestCase

from apps.core.models import Finca
from apps.produccion.models import Metrica, VariableMetrica
from apps.produccion.services.descubrimiento import (
    DescubridorMetricas,
    MetricaNoDisponible,
)


class DescubrimientoMetricasTests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca M04")

    def test_descubre_metrica_configurada_por_codigo(self):
        metrica = Metrica.objects.create(
            finca=self.finca,
            nombre="Índice de prueba",
            codigo="M04_TEST",
            categoria="productividad",
            unidad_resultado="indice",
            formula="A / B",
            version=3,
        )
        VariableMetrica.objects.create(
            metrica=metrica,
            nombre="Variable A",
            codigo="A",
            tipo="dato",
        )
        VariableMetrica.objects.create(
            metrica=metrica,
            nombre="Variable B",
            codigo="B",
            tipo="dato",
        )

        definicion = DescubridorMetricas().descubrir("M04_TEST", self.finca)

        self.assertEqual(definicion.codigo, "M04_TEST")
        self.assertEqual(definicion.version, "3")
        self.assertEqual(definicion.estrategia["modo"], "formula")
        self.assertEqual(definicion.formula, "A / B")
        self.assertEqual(definicion.dependencias, [])

    def test_no_descubre_metrica_inactiva(self):
        Metrica.objects.create(
            finca=self.finca,
            nombre="Inactiva",
            codigo="M04_OFF",
            activa=False,
        )

        with self.assertRaises(MetricaNoDisponible):
            DescubridorMetricas().descubrir("M04_OFF", self.finca)

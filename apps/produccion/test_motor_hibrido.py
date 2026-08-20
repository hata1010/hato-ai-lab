from django.test import TestCase

from apps.core.models import Finca
from apps.produccion.models import Metrica, VariableMetrica
from apps.produccion.services.motor_hibrido import (
    MotorMetricasHibrido,
    MetricaNoEncontrada,
)


class MotorMetricasHibridoTests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca M05")
        self.motor = MotorMetricasHibrido()

    def test_ejecuta_metrica_preinstalada_del_catalogo(self):
        resultado = self.motor.ejecutar(
            "CARGA_ANIMAL_HA",
            {"animales": 120, "hectareas": 60},
            finca=self.finca,
        )

        self.assertTrue(resultado.exito)
        self.assertEqual(resultado.valor, 2)
        self.assertEqual(resultado.codigo, "CARGA_ANIMAL_HA")

    def test_ejecuta_metrica_creada_en_bd(self):
        metrica = Metrica.objects.create(
            finca=self.finca,
            nombre="Índice configurable",
            codigo="M05_CONFIG",
            categoria="productividad",
            unidad_resultado="indice",
            formula="A / B",
            version=1,
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

        resultado = self.motor.ejecutar(
            "M05_CONFIG",
            {"A": 100, "B": 4},
            finca=self.finca,
        )

        self.assertTrue(resultado.exito)
        self.assertEqual(resultado.valor, 25)
        self.assertEqual(resultado.codigo, "M05_CONFIG")

    def test_metrica_bd_tiene_precedencia_sobre_catalogo(self):
        Metrica.objects.create(
            finca=self.finca,
            nombre="Cantidad personalizada",
            codigo="CANT_ANIMALES_TOTAL",
            categoria="ganado",
            unidad_resultado="animales",
            formula="A * 2",
        )

        resultado = self.motor.ejecutar(
            "CANT_ANIMALES_TOTAL",
            {"A": 7},
            finca=self.finca,
        )

        self.assertTrue(resultado.exito)
        self.assertEqual(resultado.valor, 14)

    def test_falla_si_no_existe_en_bd_ni_catalogo(self):
        with self.assertRaises(MetricaNoEncontrada):
            self.motor.descubrir("M05_NO_EXISTE", finca=self.finca)

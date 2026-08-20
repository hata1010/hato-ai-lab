"""Suite de pruebas para la Página de Definición y Administración de Métricas V1."""

import unittest
from datetime import date
from decimal import Decimal
from typing import Optional

from apps.produccion.engine.catalogo_v1 import obtener_metrica_v1
from apps.produccion.engine.ejecutor import EjecutorMotorV1
from apps.core.test_security_tenant import MockUser, MockFinca, MockUsuarioFinca
from apps.produccion.test_motor_v1 import MockAnimal, MockPesaje


class MockMetricaDB:
    def __init__(
        self,
        id: int,
        nombre: str,
        codigo: str,
        finca: Optional[MockFinca] = None,
        categoria: str = "productividad",
        unidad_resultado: str = "animales",
        activa: bool = True,
    ):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.finca = finca
        self.categoria = categoria
        self.unidad_resultado = unidad_resultado
        self.activa = activa


class TestAdminMetricasV1(unittest.TestCase):
    def setUp(self):
        self.ejecutor = EjecutorMotorV1()
        self.finca_a = MockFinca(101, "Hato San José")
        self.finca_b = MockFinca(102, "Hato El Progreso")
        self.user_juan = MockUser(2, "juan_admin", is_superuser=False)
        self.user_root = MockUser(1, "root_admin", is_superuser=True)
        self.membresias = [
            MockUsuarioFinca(self.user_juan, self.finca_a, rol="administrador", activa=True)
        ]
        self.metrica_global = MockMetricaDB(1, "Conteo Global", "CANT_ANIMALES_TOTAL", finca=None)
        self.metrica_finca_a = MockMetricaDB(2, "GMD San José", "GMD_INDIVIDUAL", finca=self.finca_a, unidad_resultado="kg/dia")
        self.metrica_finca_b = MockMetricaDB(3, "Peso El Progreso", "PESO_PROMEDIO_FINCA", finca=self.finca_b, unidad_resultado="kg")
        self.animales_finca_a = [
            MockAnimal("H001", "H", "activo", pesajes=[
                MockPesaje(Decimal("225.00"), date(2026, 7, 1)),
                MockPesaje(Decimal("200.00"), date(2026, 6, 1)),
            ]),
        ]

    def test_01_crear_definicion_metrica_local(self):
        nueva = MockMetricaDB(
            id=10,
            nombre="Biomasa Local",
            codigo="PESO_TOTAL_FINCA",
            finca=self.finca_a,
            unidad_resultado="kg",
            activa=True,
        )
        self.assertEqual(nueva.nombre, "Biomasa Local")
        self.assertEqual(nueva.codigo, "PESO_TOTAL_FINCA")
        self.assertEqual(nueva.finca.id, 101)
        self.assertTrue(nueva.activa)

    def test_02_toggle_estado_activa(self):
        metrica = self.metrica_finca_a
        self.assertTrue(metrica.activa)
        metrica.activa = not metrica.activa
        self.assertFalse(metrica.activa)
        metrica.activa = not metrica.activa
        self.assertTrue(metrica.activa)

    def test_03_usuario_finca_a_no_puede_acceder_metricas_finca_b(self):
        metricas_todas = [self.metrica_global, self.metrica_finca_a, self.metrica_finca_b]
        metricas_visibles_juan = [
            m for m in metricas_todas
            if m.finca is None or m.finca.id == self.finca_a.id
        ]
        self.assertIn(self.metrica_global, metricas_visibles_juan)
        self.assertIn(self.metrica_finca_a, metricas_visibles_juan)
        self.assertNotIn(self.metrica_finca_b, metricas_visibles_juan)

    def test_04_probar_metrica_ejecuta_motor_v1(self):
        metrica_def = obtener_metrica_v1(self.metrica_finca_a.codigo)
        animal_a001 = self.animales_finca_a[0]
        resultado = self.ejecutor.ejecutar(metrica_def, animal_a001)
        self.assertTrue(resultado.es_valido)
        self.assertEqual(resultado.valor, Decimal("0.833"))
        self.assertEqual(resultado.unidad, "kg/dia")

    def test_05_catalogo_oficial_v1_completo_para_seleccion(self):
        codigos_esperados = [
            "CANT_ANIMALES_TOTAL",
            "CANT_ANIMALES_ACTIVOS",
            "ANIMALES_POR_SEXO",
            "PESO_PROMEDIO_FINCA",
            "PESO_TOTAL_FINCA",
            "GMD_INDIVIDUAL",
            "SUP_TOTAL_POTREROS",
            "CARGA_ANIMAL_HA",
        ]
        for codigo in codigos_esperados:
            def_obj = obtener_metrica_v1(codigo)
            self.assertIsNotNone(def_obj)
            self.assertEqual(def_obj.codigo, codigo)


if __name__ == "__main__":
    unittest.main()

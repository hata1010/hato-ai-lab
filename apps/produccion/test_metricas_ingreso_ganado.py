from datetime import date

from django.test import TestCase

from apps.core.models import Finca
from apps.ganado.models import Animal, Especie, ProcedenciaAnimal
from apps.produccion.engine import EjecutorMotorV1, obtener_metrica_v1


class MetricasIngresoGanadoTests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca Métricas Ingreso")
        self.especie = Especie.objects.create(nombre="Bovino Métricas Ingreso")

        self.nacido = Animal.objects.create(
            numero_arete="MET-N-001",
            fecha_nacimiento=date(2026, 8, 25),
            sexo="M",
            especie=self.especie,
            finca=self.finca,
        )
        ProcedenciaAnimal.objects.create(
            animal=self.nacido,
            tipo="nacimiento_granja",
            fecha=date(2026, 8, 25),
            origen_nombre="Finca Métricas Ingreso",
        )

        self.adquirido = Animal.objects.create(
            numero_arete="MET-C-001",
            fecha_nacimiento=date(2024, 3, 15),
            sexo="H",
            especie=self.especie,
            finca=self.finca,
        )
        ProcedenciaAnimal.objects.create(
            animal=self.adquirido,
            tipo="compra",
            fecha=date(2026, 8, 25),
            origen_nombre="Proveedor de prueba",
        )

    def test_animales_nacidos_cuenta_solo_nacimiento_granja(self):
        definicion = obtener_metrica_v1("ANIMALES_NACIDOS")
        resultado = EjecutorMotorV1().ejecutar(
            definicion,
            Animal.objects.filter(finca=self.finca),
        )
        self.assertTrue(resultado.es_valido)
        self.assertEqual(resultado.valor, 1)

    def test_animales_adquiridos_cuenta_solo_compra(self):
        definicion = obtener_metrica_v1("ANIMALES_ADQUIRIDOS")
        resultado = EjecutorMotorV1().ejecutar(
            definicion,
            Animal.objects.filter(finca=self.finca),
        )
        self.assertTrue(resultado.es_valido)
        self.assertEqual(resultado.valor, 1)

from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.core.models import Finca
from .models import Animal, Especie
from .models_reproduccion import (
    ControlLeche,
    EventoReproductivo,
    Lactancia,
)


class ReproduccionLactanciaModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="operador_repro",
            password="test-pass",
        )
        self.finca = Finca.objects.create(nombre="Finca Test Repro")
        self.especie = Especie.objects.create(nombre="Bovino Test")
        self.vaca = Animal.objects.create(
            numero_arete="VACA-TEST-001",
            sexo="H",
            especie=self.especie,
            finca=self.finca,
        )
        self.toro = Animal.objects.create(
            numero_arete="TORO-TEST-001",
            sexo="M",
            especie=self.especie,
            finca=self.finca,
        )

    def test_monta_natural_requiere_toro(self):
        evento = EventoReproductivo(
            finca=self.finca,
            animal=self.vaca,
            tipo_evento="servicio_monta",
            fecha=timezone.make_aware(datetime(2026, 8, 21, 10, 0)),
            metodo_reproductivo="monta_natural",
            creado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_inseminacion_requiere_codigo_semen(self):
        evento = EventoReproductivo(
            finca=self.finca,
            animal=self.vaca,
            tipo_evento="inseminacion_ia",
            fecha=timezone.make_aware(datetime(2026, 8, 21, 10, 0)),
            metodo_reproductivo="ia",
            creado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_lactancia_debe_corresponder_a_hembra_y_finca(self):
        lactancia = Lactancia(
            finca=self.finca,
            animal=self.toro,
            numero_lactancia=1,
            fecha_inicio=datetime(2026, 8, 21).date(),
            creado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            lactancia.full_clean()

    def test_control_leche_no_acepta_cantidad_negativa(self):
        lactancia = Lactancia(
            finca=self.finca,
            animal=self.vaca,
            numero_lactancia=1,
            fecha_inicio=datetime(2026, 8, 21).date(),
            creado_por=self.user,
        )
        lactancia.full_clean()
        lactancia.save()

        control = ControlLeche(
            finca=self.finca,
            lactancia=lactancia,
            fecha=timezone.make_aware(datetime(2026, 8, 21, 8, 0)),
            jornada="manana",
            cantidad=Decimal("-1.000"),
            unidad="l",
            creado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            control.full_clean()

    def test_control_leche_respeta_finca_de_lactancia(self):
        otra_finca = Finca.objects.create(nombre="Finca Test Repro 2")
        lactancia = Lactancia(
            finca=self.finca,
            animal=self.vaca,
            numero_lactancia=1,
            fecha_inicio=datetime(2026, 8, 21).date(),
            creado_por=self.user,
        )
        lactancia.full_clean()
        lactancia.save()

        control = ControlLeche(
            finca=otra_finca,
            lactancia=lactancia,
            fecha=timezone.make_aware(datetime(2026, 8, 21, 8, 0)),
            jornada="manana",
            cantidad=Decimal("10.000"),
            unidad="l",
            creado_por=self.user,
        )
        with self.assertRaises(ValidationError):
            control.full_clean()

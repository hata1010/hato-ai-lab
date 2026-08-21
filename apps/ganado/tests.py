from datetime import date, datetime, timezone
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.core.models import Finca
from apps.ganado.models import Animal, Especie
from apps.ganado.models_reproduccion import (
    ControlLeche,
    CriaNacimiento,
    EventoReproductivo,
    Lactancia,
)


class ReproduccionLactanciaBaseTestCase(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca Test Reproduccion")
        self.otra_finca = Finca.objects.create(nombre="Finca Test Otra")
        self.especie = Especie.objects.create(nombre="Bovino Test")

        self.madre = Animal.objects.create(
            numero_arete="MADRE-TEST-001",
            fecha_nacimiento=date(2022, 1, 1),
            sexo="H",
            especie=self.especie,
            finca=self.finca,
        )
        self.toro = Animal.objects.create(
            numero_arete="TORO-TEST-001",
            fecha_nacimiento=date(2021, 1, 1),
            sexo="M",
            especie=self.especie,
            finca=self.finca,
        )

    def parto(self, fecha=None):
        return EventoReproductivo.objects.create(
            finca=self.finca,
            animal=self.madre,
            tipo_evento="parto",
            fecha=fecha or datetime(2026, 8, 1, 8, 0, tzinfo=timezone.utc),
            tipo_parto="normal",
            toro=self.toro,
        )


class EventoReproductivoTests(ReproduccionLactanciaBaseTestCase):
    def test_servicio_monta_requiere_toro(self):
        evento = EventoReproductivo(
            finca=self.finca,
            animal=self.madre,
            tipo_evento="servicio_monta",
            fecha=datetime(2026, 7, 1, 8, 0, tzinfo=timezone.utc),
            metodo_reproductivo="monta_natural",
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_inseminacion_requiere_codigo_de_semen(self):
        evento = EventoReproductivo(
            finca=self.finca,
            animal=self.madre,
            tipo_evento="inseminacion_ia",
            fecha=datetime(2026, 7, 1, 8, 0, tzinfo=timezone.utc),
            metodo_reproductivo="ia",
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_evento_no_puede_cruzar_finca(self):
        evento = EventoReproductivo(
            finca=self.otra_finca,
            animal=self.madre,
            tipo_evento="parto",
            fecha=datetime(2026, 8, 1, 8, 0, tzinfo=timezone.utc),
            tipo_parto="normal",
        )
        with self.assertRaises(ValidationError):
            evento.full_clean()

    def test_parto_puede_trazar_toro_real(self):
        parto = self.parto()
        self.assertEqual(parto.toro_id, self.toro.id)
        self.assertEqual(parto.finca_id, self.finca.id)


class CriaNacimientoTests(ReproduccionLactanciaBaseTestCase):
    def test_cria_vincula_madre_y_padre_a_traves_de_animal(self):
        parto = self.parto()
        cria = Animal.objects.create(
            numero_arete="CRIA-TEST-001",
            fecha_nacimiento=date(2026, 8, 1),
            sexo="H",
            especie=self.especie,
            finca=self.finca,
            madre=self.madre,
            padre=self.toro,
        )

        nacimiento = CriaNacimiento(
            finca=self.finca,
            parto=parto,
            animal=cria,
        )
        nacimiento.full_clean()
        nacimiento.save()

        self.assertEqual(cria.madre_id, self.madre.id)
        self.assertEqual(cria.padre_id, self.toro.id)
        self.assertEqual(nacimiento.parto_id, parto.id)

    def test_cria_no_puede_pertenecer_a_otra_finca(self):
        parto = self.parto()
        cria = Animal.objects.create(
            numero_arete="CRIA-TEST-002",
            fecha_nacimiento=date(2026, 8, 1),
            sexo="H",
            especie=self.especie,
            finca=self.otra_finca,
        )
        nacimiento = CriaNacimiento(
            finca=self.finca,
            parto=parto,
            animal=cria,
        )
        with self.assertRaises(ValidationError):
            nacimiento.full_clean()


class LactanciaTests(ReproduccionLactanciaBaseTestCase):
    def test_lactancia_se_vincula_al_parto(self):
        parto = self.parto()
        lactancia = Lactancia(
            finca=self.finca,
            animal=self.madre,
            parto_origen=parto,
            numero_lactancia=1,
            fecha_inicio=date(2026, 8, 1),
        )
        lactancia.full_clean()
        lactancia.save()

        self.assertEqual(lactancia.parto_origen_id, parto.id)
        self.assertEqual(lactancia.animal_id, self.madre.id)

    def test_lactancia_secada_requiere_fecha(self):
        lactancia = Lactancia(
            finca=self.finca,
            animal=self.madre,
            numero_lactancia=1,
            fecha_inicio=date(2026, 8, 1),
            estado="secada",
        )
        with self.assertRaises(ValidationError):
            lactancia.full_clean()

    def test_lactancia_no_puede_cruzar_finca(self):
        lactancia = Lactancia(
            finca=self.otra_finca,
            animal=self.madre,
            numero_lactancia=1,
            fecha_inicio=date(2026, 8, 1),
        )
        with self.assertRaises(ValidationError):
            lactancia.full_clean()


class ControlLecheTests(ReproduccionLactanciaBaseTestCase):
    def test_control_leche_valido(self):
        lactancia = Lactancia.objects.create(
            finca=self.finca,
            animal=self.madre,
            numero_lactancia=1,
            fecha_inicio=date(2026, 8, 1),
        )
        control = ControlLeche(
            finca=self.finca,
            lactancia=lactancia,
            fecha=datetime(2026, 8, 2, 7, 0, tzinfo=timezone.utc),
            jornada="manana",
            cantidad=Decimal("12.500"),
            unidad="l",
        )
        control.full_clean()
        control.save()

        self.assertEqual(control.cantidad, Decimal("12.500"))
        self.assertEqual(control.lactancia_id, lactancia.id)

    def test_control_leche_no_puede_ser_anterior_a_lactancia(self):
        lactancia = Lactancia.objects.create(
            finca=self.finca,
            animal=self.madre,
            numero_lactancia=1,
            fecha_inicio=date(2026, 8, 10),
        )
        control = ControlLeche(
            finca=self.finca,
            lactancia=lactancia,
            fecha=datetime(2026, 8, 9, 7, 0, tzinfo=timezone.utc),
            jornada="manana",
            cantidad=Decimal("10.000"),
            unidad="l",
        )
        with self.assertRaises(ValidationError):
            control.full_clean()

    def test_control_leche_no_puede_cruzar_finca(self):
        lactancia = Lactancia.objects.create(
            finca=self.finca,
            animal=self.madre,
            numero_lactancia=1,
            fecha_inicio=date(2026, 8, 1),
        )
        control = ControlLeche(
            finca=self.otra_finca,
            lactancia=lactancia,
            fecha=datetime(2026, 8, 2, 7, 0, tzinfo=timezone.utc),
            jornada="manana",
            cantidad=Decimal("10.000"),
            unidad="l",
        )
        with self.assertRaises(ValidationError):
            control.full_clean()

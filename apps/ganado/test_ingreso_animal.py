from datetime import date, datetime, timezone
from decimal import Decimal

from django.test import TestCase

from apps.core.models import Finca, Potrero

from .forms import IngresoAnimalForm
from .models import AdquisicionAnimal, Animal, Especie, MovimientoAnimal, PesajeAnimal
from .models_reproduccion import CriaNacimiento, EventoReproductivo
from .services_ingreso import registrar_ingreso_compra, registrar_ingreso_nacimiento


class IngresoAnimalTests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca Ingreso Test")
        self.especie = Especie.objects.create(nombre="Bovino Ingreso Test")
        self.potrero = Potrero.objects.create(
            finca=self.finca,
            nombre="Maternidad",
            codigo="MAT-01",
            tipo="corral",
        )
        self.toro = Animal.objects.create(
            numero_arete="TORO-001",
            sexo="M",
            especie=self.especie,
            finca=self.finca,
        )
        self.vaca = Animal.objects.create(
            numero_arete="VACA-001",
            sexo="H",
            especie=self.especie,
            finca=self.finca,
        )

    def test_form_filtra_padre_y_madre_por_sexo(self):
        form = IngresoAnimalForm(finca=self.finca)
        self.assertIn(self.toro, form.fields["padre"].queryset)
        self.assertNotIn(self.vaca, form.fields["padre"].queryset)
        self.assertIn(self.vaca, form.fields["madre"].queryset)
        self.assertNotIn(self.toro, form.fields["madre"].queryset)

    def test_compra_crea_procedencia_adquisicion_pesaje_y_movimiento(self):
        animal = Animal(
            numero_arete="COMP-001",
            sexo="H",
            especie=self.especie,
            finca=self.finca,
            madre=self.vaca,
        )
        resultado = registrar_ingreso_compra(
            finca=self.finca,
            animal=animal,
            proveedor="Mercado Z",
            fecha_compra=date(2026, 8, 25),
            documento_compra="F-500",
            precio_individual=Decimal("400.00"),
            peso_inicial=Decimal("250.00"),
            potrero_inicial=self.potrero,
        )

        self.assertEqual(resultado.id, animal.id)
        self.assertEqual(animal.procedencia.tipo, "compra")
        self.assertEqual(AdquisicionAnimal.objects.get(animal=animal).precio_individual, Decimal("400.00"))
        self.assertEqual(PesajeAnimal.objects.get(animal=animal).peso_kg, Decimal("250.00"))
        self.assertEqual(MovimientoAnimal.objects.get(animal=animal).potrero_id, self.potrero.id)

    def test_nacimiento_crea_parto_cria_pesaje_y_movimiento(self):
        animal = Animal(
            numero_arete="CRIA-001",
            sexo="M",
            especie=self.especie,
            finca=self.finca,
        )
        momento = datetime(2026, 8, 25, 10, 30, tzinfo=timezone.utc)
        resultado = registrar_ingreso_nacimiento(
            finca=self.finca,
            animal=animal,
            madre=self.vaca,
            padre=self.toro,
            fecha_parto=momento,
            tipo_parto="normal",
            peso_inicial=Decimal("35.00"),
            potrero_inicial=self.potrero,
        )

        self.assertEqual(resultado.madre_id, self.vaca.id)
        self.assertEqual(resultado.padre_id, self.toro.id)
        parto = EventoReproductivo.objects.get(tipo_evento="parto", animal=self.vaca)
        self.assertEqual(parto.toro_id, self.toro.id)
        nacimiento = CriaNacimiento.objects.get(animal=animal)
        self.assertEqual(nacimiento.parto_id, parto.id)
        self.assertEqual(PesajeAnimal.objects.get(animal=animal).peso_kg, Decimal("35.00"))
        self.assertEqual(MovimientoAnimal.objects.get(animal=animal).potrero_id, self.potrero.id)
        self.assertEqual(animal.procedencia.tipo, "nacimiento_granja")

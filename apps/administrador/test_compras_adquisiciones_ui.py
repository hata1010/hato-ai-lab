from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Finca
from apps.ganado.models import Adquisicion, Animal, Especie, AdquisicionAnimal


class ComprasAdquisicionesUITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="compras-ui-user",
            password="test-pass",
        )
        self.finca = Finca.objects.create(nombre="Finca Compras UI")
        self.especie = Especie.objects.create(nombre="Bovino Compras UI")
        self.animal = Animal.objects.create(
            numero_arete="COMP-001",
            fecha_nacimiento=date(2022, 1, 1),
            sexo="H",
            especie=self.especie,
            finca=self.finca,
        )
        self.adquisicion = Adquisicion.objects.create(
            finca=self.finca,
            proveedor="Proveedor UI",
            fecha=date(2026, 8, 25),
            numero_documento="FAC-001",
            costo_total=Decimal("1250000.00"),
        )
        AdquisicionAnimal.objects.create(
            adquisicion=self.adquisicion,
            animal=self.animal,
            precio_individual=Decimal("1250000.00"),
        )
        self.client.force_login(self.user)

    def tenant_context(self):
        return patch.multiple(
            "apps.administrador.compras_views",
            obtener_finca_activa=lambda request: self.finca,
            verificar_acceso_finca=lambda user, finca: True,
        )

    def test_menu_y_pantalla_de_compras_son_accesibles(self):
        with self.tenant_context():
            response = self.client.get(reverse("administrador:compras_adquisiciones"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Compras y adquisiciones")
        self.assertContains(response, "Compra de animales")
        self.assertContains(response, "Adquisición de suministros")
        self.assertContains(response, "Proveedor UI")
        self.assertContains(response, "FAC-001")
        self.assertContains(response, reverse("admin:ganado_adquisicion_changelist"))
        self.assertContains(response, reverse("admin:ganado_adquisicion_add"))

    def test_pantalla_no_expone_adquisiciones_de_otra_finca(self):
        otra_finca = Finca.objects.create(nombre="Finca Otra Compras UI")
        Adquisicion.objects.create(
            finca=otra_finca,
            proveedor="Proveedor Otra Finca",
            fecha=date(2026, 8, 25),
            costo_total=Decimal("500000.00"),
        )
        with self.tenant_context():
            response = self.client.get(reverse("administrador:compras_adquisiciones"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Proveedor UI")
        self.assertNotContains(response, "Proveedor Otra Finca")

from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Finca
from apps.ganado.models import Animal, Especie, PesajeAnimal


class PesajesUITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="pesaje-ui-user", password="test-pass")
        self.finca = Finca.objects.create(nombre="Finca Pesaje UI")
        self.otra_finca = Finca.objects.create(nombre="Finca Otra UI")
        self.especie = Especie.objects.create(nombre="Bovino Pesaje UI")
        self.animal = Animal.objects.create(numero_arete="PR-D-001", fecha_nacimiento=date(2022, 1, 1), sexo="H", especie=self.especie, finca=self.finca)
        self.otro_animal = Animal.objects.create(numero_arete="OTRA-001", fecha_nacimiento=date(2022, 1, 1), sexo="M", especie=self.especie, finca=self.otra_finca)
        self.client.force_login(self.user)

    def tenant_context(self):
        return patch.multiple("apps.ganado.pesaje_views", obtener_finca_activa=lambda request: self.finca, verificar_acceso_finca=lambda user, finca: True, obtener_rol_usuario_finca=lambda user, finca: "administrador")

    def test_lista_pesajes_es_accesible(self):
        with self.tenant_context():
            response = self.client.get(reverse("ganado:lista_pesajes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "⚖️ Pesajes")
        self.assertContains(response, "Registrar pesaje")

    def test_crear_pesaje_guarda_registro_y_redirige_a_historial(self):
        with self.tenant_context():
            response = self.client.post(reverse("ganado:crear_pesaje"), {"animal": self.animal.id, "fecha": "2026-08-24T10:30", "peso_kg": "450.50", "observaciones": "Control de prueba"})
        self.assertEqual(response.status_code, 302)
        pesaje = PesajeAnimal.objects.get(animal=self.animal)
        self.assertEqual(pesaje.peso_kg, Decimal("450.50"))
        self.assertEqual(response.url, reverse("ganado:historial_pesajes_animal", args=[self.animal.id]))

    def test_historial_muestra_pesaje_del_animal(self):
        PesajeAnimal.objects.create(animal=self.animal, fecha="2026-08-24T10:30Z", peso_kg=Decimal("450.50"), observaciones="Historial UI")
        with self.tenant_context():
            response = self.client.get(reverse("ganado:historial_pesajes_animal", args=[self.animal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "450.50")
        self.assertContains(response, "Historial UI")

    def test_historial_no_permite_acceso_a_animal_de_otra_finca(self):
        with self.tenant_context():
            response = self.client.get(reverse("ganado:historial_pesajes_animal", args=[self.otro_animal.id]))
        self.assertEqual(response.status_code, 404)

    def test_ficha_animal_expone_navegacion_de_pesajes(self):
        with self.tenant_context():
            response = self.client.get(reverse("ganado:detalle_animal", args=[self.animal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("ganado:historial_pesajes_animal", args=[self.animal.id]))
        self.assertContains(response, reverse("ganado:crear_pesaje") + f"?animal={self.animal.id}")

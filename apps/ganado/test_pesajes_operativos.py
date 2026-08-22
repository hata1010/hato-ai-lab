from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Finca, UsuarioFinca

from .models import Animal, Especie, PesajeAnimal


class PesajesOperativosTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username="adminpes", password="x")
        self.operador = User.objects.create_user(username="operadorpes", password="x")
        self.finca = Finca.objects.create(nombre="Finca Pesajes")
        self.otro_finca = Finca.objects.create(nombre="Otra Finca")
        UsuarioFinca.objects.create(usuario=self.admin, finca=self.finca, rol="administrador")
        UsuarioFinca.objects.create(usuario=self.operador, finca=self.finca, rol="operador")
        self.especie = Especie.objects.create(nombre="Bovino")
        self.animal = Animal.objects.create(numero_arete="P-001", sexo="H", especie=self.especie, finca=self.finca)
        self.otro_animal = Animal.objects.create(numero_arete="P-002", sexo="M", especie=self.especie, finca=self.otro_finca)
        self.client.force_login(self.admin)
        session = self.client.session
        session["finca_activa_id"] = self.finca.id
        session.save()

    def test_menu_url_de_pesajes_existe(self):
        response = self.client.get(reverse("ganado:lista_pesajes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pesajes")

    def test_administrador_puede_ver_y_crear(self):
        response = self.client.post(reverse("ganado:crear_pesaje"), {
            "animal": self.animal.id,
            "fecha": "2026-08-21T10:00",
            "peso_kg": "425.50",
            "observaciones": "Pesaje de control",
        })
        self.assertRedirects(response, reverse("ganado:detalle_animal", args=[self.animal.id]))
        self.assertTrue(PesajeAnimal.objects.filter(animal=self.animal, peso_kg=Decimal("425.50")).exists())

    def test_operador_puede_consultar_pero_no_gestionar(self):
        self.client.force_login(self.operador)
        self.assertEqual(self.client.get(reverse("ganado:lista_pesajes")).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:crear_pesaje")).status_code, 403)

    def test_pesaje_no_cruza_de_finca(self):
        response = self.client.post(reverse("ganado:crear_pesaje"), {
            "animal": self.otro_animal.id,
            "fecha": "2026-08-21T10:00",
            "peso_kg": "500",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PesajeAnimal.objects.filter(animal=self.otro_animal).exists())

    def test_peso_debe_ser_positivo(self):
        response = self.client.post(reverse("ganado:crear_pesaje"), {
            "animal": self.animal.id,
            "fecha": "2026-08-21T10:00",
            "peso_kg": "0",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PesajeAnimal.objects.filter(animal=self.animal).exists())

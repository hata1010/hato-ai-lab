from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Finca, UsuarioFinca

from .models import Animal, Especie


class AnimalesOperativosTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin_finca")
        self.operador = User.objects.create_user("operador_finca")
        self.otra_finca = Finca.objects.create(nombre="Otra Finca")
        self.finca = Finca.objects.create(nombre="Finca Operativa")
        UsuarioFinca.objects.create(usuario=self.admin, finca=self.finca, rol="administrador")
        UsuarioFinca.objects.create(usuario=self.operador, finca=self.finca, rol="operador")
        self.especie = Especie.objects.create(nombre="Bovino")
        self.animal = Animal.objects.create(
            finca=self.finca,
            numero_arete="A-001",
            sexo="H",
            especie=self.especie,
        )

    def test_menu_url_existe(self):
        self.assertEqual(reverse("ganado:lista_animales"), "/ganado/animales/")

    def test_administrador_puede_ver_y_crear(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("ganado:lista_animales"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("ganado:crear_animal"))
        self.assertEqual(response.status_code, 200)

    def test_operador_puede_consultar_pero_no_gestionar(self):
        self.client.force_login(self.operador)
        self.assertEqual(self.client.get(reverse("ganado:lista_animales")).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:crear_animal")).status_code, 403)
        self.assertEqual(self.client.get(reverse("ganado:editar_animal", args=[self.animal.id])).status_code, 403)

    def test_ficha_no_cruza_de_finca(self):
        otra_especie = Especie.objects.create(nombre="Otra especie")
        animal_otra_finca = Animal.objects.create(
            finca=self.otra_finca,
            numero_arete="B-001",
            sexo="M",
            especie=otra_especie,
        )
        self.client.force_login(self.admin)
        response = self.client.get(reverse("ganado:detalle_animal", args=[animal_otra_finca.id]))
        self.assertEqual(response.status_code, 404)

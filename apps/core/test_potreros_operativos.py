from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Finca, Potrero, UsuarioFinca


class PotrerosOperativosTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin_potrero", password="secret")
        self.operador = User.objects.create_user("operador_potrero", password="secret")
        self.finca = Finca.objects.create(nombre="Finca Operativa", created_by=self.admin)
        UsuarioFinca.objects.create(usuario=self.admin, finca=self.finca, rol="administrador")
        UsuarioFinca.objects.create(usuario=self.operador, finca=self.finca, rol="operador")
        self.potrero = Potrero.objects.create(
            finca=self.finca,
            nombre="Potrero Norte",
            codigo="PN-01",
        )

    def test_menu_url_de_potreros_existe(self):
        self.assertEqual(reverse("potreros:lista"), "/potreros/")
        self.assertEqual(reverse("potreros:crear"), "/potreros/crear/")
        self.assertEqual(
            reverse("potreros:detalle", args=[self.potrero.id]),
            f"/potreros/{self.potrero.id}/",
        )

    def test_administrador_puede_consultar_y_crear(self):
        self.client.login(username="admin_potrero", password="secret")
        response = self.client.get(reverse("potreros:lista"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("potreros:crear"),
            {
                "nombre": "Potrero Sur",
                "codigo": "PS-01",
                "tipo": "potrero",
                "capacidad_animales": "20",
                "carga_actual": "0",
                "tipo_pasto": "Brachiaria",
                "calidad_pasto": "bueno",
                "estado": "disponible",
                "dias_descanso": "0",
                "descripcion": "Creado desde Hato",
                "is_active": "on",
                "ubicacion_wkt": "",
                "poligono_wkt": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Potrero.objects.filter(codigo="PS-01", finca=self.finca).exists())

    def test_operador_puede_consultar_pero_no_gestionar(self):
        self.client.login(username="operador_potrero", password="secret")
        self.assertEqual(self.client.get(reverse("potreros:lista")).status_code, 200)
        self.assertEqual(self.client.get(reverse("potreros:crear")).status_code, 403)
        self.assertEqual(self.client.get(reverse("potreros:editar", args=[self.potrero.id])).status_code, 403)

    def test_potrero_de_otra_finca_no_es_accesible(self):
        otra_finca = Finca.objects.create(nombre="Otra Finca")
        otro_potrero = Potrero.objects.create(
            finca=otra_finca,
            nombre="Potrero Ajeno",
            codigo="PA-01",
        )
        self.client.login(username="admin_potrero", password="secret")
        response = self.client.get(reverse("potreros:detalle", args=[otro_potrero.id]))
        self.assertEqual(response.status_code, 404)

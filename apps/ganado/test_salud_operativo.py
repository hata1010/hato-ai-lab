from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Finca, UsuarioFinca

from .models import Animal, Especie, EventoSalud


class SaludOperativaTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin_salud")
        self.operador = User.objects.create_user("operador_salud")
        self.finca = Finca.objects.create(nombre="Finca Salud")
        self.otra_finca = Finca.objects.create(nombre="Otra Finca Salud")
        UsuarioFinca.objects.create(usuario=self.admin, finca=self.finca, rol="administrador")
        UsuarioFinca.objects.create(usuario=self.operador, finca=self.finca, rol="operador")
        self.especie = Especie.objects.create(nombre="Bovino Salud")
        self.animal = Animal.objects.create(
            finca=self.finca,
            numero_arete="SALUD-001",
            sexo="H",
            especie=self.especie,
        )
        self.evento = EventoSalud.objects.create(
            animal=self.animal,
            tipo="consulta",
            fecha=datetime(2026, 8, 21, 9, 0, tzinfo=timezone.utc),
            nombre_veterinario="Dra. Test",
            observaciones="Revisión preventiva",
        )

    def test_urls_de_salud_existen(self):
        self.assertEqual(reverse("ganado:lista_salud"), "/ganado/salud/")
        self.assertEqual(
            reverse("ganado:historia_salud_animal", args=[self.animal.id]),
            f"/ganado/salud/animal/{self.animal.id}/",
        )

    def test_administrador_puede_consultar_y_crear(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("ganado:lista_salud")).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:historia_salud_animal", args=[self.animal.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:crear_evento_salud")).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:editar_evento_salud", args=[self.evento.id])).status_code, 200)

    def test_operador_puede_consultar_pero_no_gestionar(self):
        self.client.force_login(self.operador)
        self.assertEqual(self.client.get(reverse("ganado:lista_salud")).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:historia_salud_animal", args=[self.animal.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:crear_evento_salud")).status_code, 403)
        self.assertEqual(self.client.get(reverse("ganado:editar_evento_salud", args=[self.evento.id])).status_code, 403)

    def test_historia_no_cruza_de_finca(self):
        otro_animal = Animal.objects.create(
            finca=self.otra_finca,
            numero_arete="SALUD-OTRA-001",
            sexo="M",
            especie=self.especie,
        )
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("ganado:historia_salud_animal", args=[otro_animal.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_evento_creado_queda_vinculado_a_animal_de_finca_activa(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("ganado:crear_evento_salud"),
            {
                "animal": self.animal.id,
                "tipo": "vacunacion",
                "fecha": "2026-08-21T10:30",
                "producto": "Vacuna Test",
                "dosis": "5 ml",
                "nombre_veterinario": "Dr. Test",
                "observaciones": "Aplicación preventiva",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            EventoSalud.objects.filter(
                animal=self.animal,
                tipo="vacunacion",
                producto="Vacuna Test",
            ).exists()
        )

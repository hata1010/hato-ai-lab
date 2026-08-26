from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Finca, UsuarioFinca

from .animal_edit_form import AnimalEditForm
from .models import Animal, Especie


User = get_user_model()


class AnimalEditUITests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca Alfa")
        self.otra_finca = Finca.objects.create(nombre="Finca Beta")

        self.admin = User.objects.create_user(username="admin_edit", password="password")
        UsuarioFinca.objects.create(
            usuario=self.admin,
            finca=self.finca,
            rol="administrador",
        )

        self.consultor = User.objects.create_user(username="consultor_edit", password="password")
        UsuarioFinca.objects.create(
            usuario=self.consultor,
            finca=self.finca,
            rol="auditor",
        )

        self.bovino = Especie.objects.create(nombre="Bovino")
        self.equino = Especie.objects.create(nombre="Equino")

        self.toro = Animal.objects.create(
            finca=self.finca,
            numero_arete="T-EDIT-01",
            sexo="M",
            especie=self.bovino,
        )
        self.vaca = Animal.objects.create(
            finca=self.finca,
            numero_arete="V-EDIT-01",
            sexo="H",
            especie=self.bovino,
        )
        self.caballo = Animal.objects.create(
            finca=self.finca,
            numero_arete="C-EDIT-01",
            sexo="M",
            especie=self.equino,
        )
        self.objetivo = Animal.objects.create(
            finca=self.finca,
            numero_arete="PR-D-012",
            nombre_propio="Dato diverso PR-D-012",
            sexo="M",
            especie=self.bovino,
            estado="activo",
            is_active=True,
        )
        self.ajeno = Animal.objects.create(
            finca=self.otra_finca,
            numero_arete="V-BETA-01",
            sexo="H",
            especie=self.bovino,
        )

    def _set_finca_activa(self, client, finca):
        session = client.session
        session["finca_activa_id"] = finca.id
        session.save()

    def _login_admin(self):
        self.client.login(username="admin_edit", password="password")
        self._set_finca_activa(self.client, self.finca)

    def test_editar_muestra_tarjetas_y_enlaces_existentes(self):
        self._login_admin()
        response = self.client.get(
            reverse("ganado:editar_animal", args=[self.objetivo.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Identificación Principal")
        self.assertContains(response, "Biología y Genética")
        self.assertContains(response, "Registros y Marcas")
        self.assertContains(response, "Estado y Observaciones")
        self.assertContains(response, "Historia y navegación del animal")
        self.assertContains(response, reverse("ganado:historia_salud_animal", args=[self.objetivo.id]))
        self.assertContains(response, "Guardar Cambios")

    def test_padre_madre_se_filtran_por_finca_especie_y_sexo(self):
        self._login_admin()
        response = self.client.get(
            reverse("ganado:editar_animal", args=[self.objetivo.id])
        )
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        padre_ids = {choice[0] for choice in form.fields["padre"].choices if choice[0]}
        madre_ids = {choice[0] for choice in form.fields["madre"].choices if choice[0]}

        self.assertIn(self.toro.id, padre_ids)
        self.assertNotIn(self.vaca.id, padre_ids)
        self.assertNotIn(self.caballo.id, padre_ids)
        self.assertNotIn(self.objetivo.id, padre_ids)
        self.assertNotIn(self.ajeno.id, madre_ids)
        self.assertIn(self.vaca.id, madre_ids)
        self.assertNotIn(self.toro.id, madre_ids)
        self.assertNotIn(self.objetivo.id, madre_ids)

    def test_edicion_exitosa(self):
        self._login_admin()
        response = self.client.post(
            reverse("ganado:editar_animal", args=[self.objetivo.id]),
            {
                "numero_arete": "PR-D-012-M",
                "nombre_propio": "Animal Editado",
                "sexo": "M",
                "categoria": "Toro reproductor",
                "estado": "activo",
                "especie": self.bovino.id,
                "fecha_nacimiento": "2018-08-16",
                "padre": self.toro.id,
                "madre": self.vaca.id,
                "observaciones": "Edición controlada.",
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.objetivo.refresh_from_db()
        self.assertEqual(self.objetivo.numero_arete, "PR-D-012-M")
        self.assertEqual(self.objetivo.nombre_propio, "Animal Editado")
        self.assertEqual(self.objetivo.padre_id, self.toro.id)
        self.assertEqual(self.objetivo.madre_id, self.vaca.id)

    def test_estado_inactivo_forza_is_active_false(self):
        self._login_admin()
        response = self.client.post(
            reverse("ganado:editar_animal", args=[self.objetivo.id]),
            {
                "numero_arete": self.objetivo.numero_arete,
                "nombre_propio": self.objetivo.nombre_propio,
                "sexo": "M",
                "categoria": "Toro reproductor",
                "estado": "vendido",
                "especie": self.bovino.id,
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.objetivo.refresh_from_db()
        self.assertEqual(self.objetivo.estado, "vendido")
        self.assertFalse(self.objetivo.is_active)

    def test_usuario_sin_permiso_recibe_403(self):
        self.client.login(username="consultor_edit", password="password")
        self._set_finca_activa(self.client, self.finca)

        response = self.client.get(
            reverse("ganado:editar_animal", args=[self.objetivo.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_animal_de_otra_finca_no_es_accesible(self):
        self._login_admin()
        response = self.client.get(
            reverse("ganado:editar_animal", args=[self.ajeno.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_form_rechaza_padre_de_otra_especie(self):
        form = AnimalEditForm(
            data={
                "numero_arete": self.objetivo.numero_arete,
                "nombre_propio": self.objetivo.nombre_propio,
                "sexo": "M",
                "categoria": "Toro reproductor",
                "estado": "activo",
                "especie": self.bovino.id,
                "padre": self.caballo.id,
                "is_active": "on",
            },
            instance=self.objetivo,
            finca=self.finca,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("padre", form.errors)
        self.assertIn("misma especie", str(form.errors["padre"]))

    def test_cambio_de_especie_no_acepta_padre_de_especie_anterior(self):
        form = AnimalEditForm(
            data={
                "numero_arete": self.objetivo.numero_arete,
                "nombre_propio": self.objetivo.nombre_propio,
                "sexo": "M",
                "categoria": "Reproductor",
                "estado": "activo",
                "especie": self.equino.id,
                "padre": self.toro.id,
                "is_active": "on",
            },
            instance=self.objetivo,
            finca=self.finca,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("padre", form.errors)

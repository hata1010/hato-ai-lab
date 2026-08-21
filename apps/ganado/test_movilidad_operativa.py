from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.core.models import Finca, Potrero, UsuarioFinca

from .models import Animal, Especie, MovimientoAnimal


class MovilidadOperativaTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username="adminmov", password="x")
        self.operador = User.objects.create_user(username="operadormov", password="x")
        self.otra_admin = User.objects.create_user(username="adminotra", password="x")
        self.finca = Finca.objects.create(nombre="Finca Movilidad")
        self.otra_finca = Finca.objects.create(nombre="Otra Finca")
        UsuarioFinca.objects.create(usuario=self.admin, finca=self.finca, rol="administrador")
        UsuarioFinca.objects.create(usuario=self.operador, finca=self.finca, rol="operador")
        UsuarioFinca.objects.create(usuario=self.otra_admin, finca=self.otra_finca, rol="administrador")
        self.potrero = Potrero.objects.create(finca=self.finca, nombre="Potrero 1", codigo="P1")
        self.otro_potrero = Potrero.objects.create(finca=self.otra_finca, nombre="Potrero B", codigo="PB")
        self.especie = Especie.objects.create(nombre="Bovino movilidad")
        self.animal = Animal.objects.create(finca=self.finca, numero_arete="MOV-001", sexo="H", especie=self.especie)
        self.otro_animal = Animal.objects.create(finca=self.otra_finca, numero_arete="MOV-002", sexo="M", especie=self.especie)

    def _activar_finca(self, finca):
        session = self.client.session
        session["finca_activa_id"] = finca.id
        session.save()

    def test_menu_y_listado_existen(self):
        self.client.force_login(self.admin)
        self._activar_finca(self.finca)
        response = self.client.get(reverse("ganado:lista_movilidad"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movilidad del ganado")

    def test_administrador_puede_crear_movimiento(self):
        self.client.force_login(self.admin)
        self._activar_finca(self.finca)
        response = self.client.post(reverse("ganado:crear_movimiento"), {
            "animal": self.animal.id,
            "potrero": self.potrero.id,
            "fecha_entrada": "2026-08-21T10:00",
            "observaciones": "Entrada al potrero 1",
        })
        self.assertEqual(response.status_code, 302)
        movimiento = MovimientoAnimal.objects.get(animal=self.animal)
        self.assertEqual(movimiento.potrero_id, self.potrero.id)
        self.assertTrue(movimiento.activo)

    def test_operador_consulta_pero_no_gestiona(self):
        self.client.force_login(self.operador)
        self._activar_finca(self.finca)
        self.assertEqual(self.client.get(reverse("ganado:lista_movilidad")).status_code, 200)
        self.assertEqual(self.client.get(reverse("ganado:crear_movimiento")).status_code, 403)

    def test_no_cruza_animales_ni_potreros_de_otra_finca(self):
        self.client.force_login(self.admin)
        self._activar_finca(self.finca)
        response = self.client.get(reverse("ganado:historial_movilidad_animal", args=[self.otro_animal.id]))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("ganado:crear_movimiento"), {
            "animal": self.animal.id,
            "potrero": self.otro_potrero.id,
            "fecha_entrada": "2026-08-21T10:00",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(MovimientoAnimal.objects.exists())

    def test_un_solo_movimiento_activo_por_animal(self):
        self.client.force_login(self.admin)
        self._activar_finca(self.finca)
        self.client.post(reverse("ganado:crear_movimiento"), {
            "animal": self.animal.id,
            "potrero": self.potrero.id,
            "fecha_entrada": "2026-08-21T10:00",
        })
        otro_potrero = Potrero.objects.create(finca=self.finca, nombre="Potrero 2", codigo="P2")
        response = self.client.post(reverse("ganado:crear_movimiento"), {
            "animal": self.animal.id,
            "potrero": otro_potrero.id,
            "fecha_entrada": "2026-08-21T12:00",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MovimientoAnimal.objects.filter(animal=self.animal, activo=True).count(), 1)

    def test_cerrar_movimiento_registra_salida(self):
        movimiento = MovimientoAnimal.objects.create(
            animal=self.animal, potrero=self.potrero,
            fecha_entrada=timezone.now(), activo=True,
        )
        self.client.force_login(self.admin)
        self._activar_finca(self.finca)
        response = self.client.post(reverse("ganado:cerrar_movimiento", args=[movimiento.id]))
        self.assertEqual(response.status_code, 302)
        movimiento.refresh_from_db()
        self.assertFalse(movimiento.activo)
        self.assertIsNotNone(movimiento.fecha_salida)

    def test_no_puede_cerrar_movimiento_de_otra_finca(self):
        movimiento = MovimientoAnimal.objects.create(
            animal=self.otro_animal, potrero=self.otro_potrero,
            fecha_entrada=timezone.now(), activo=True,
        )
        self.client.force_login(self.admin)
        self._activar_finca(self.finca)
        response = self.client.post(reverse("ganado:cerrar_movimiento", args=[movimiento.id]))
        self.assertEqual(response.status_code, 404)
        movimiento.refresh_from_db()
        self.assertTrue(movimiento.activo)

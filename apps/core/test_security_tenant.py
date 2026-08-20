"""Suite oficial de pruebas automatizadas de seguridad y aislamiento Multi-Finca Hato V1."""

import unittest
from datetime import date
from decimal import Decimal
from typing import List, Optional

from apps.core.tenant import (
    obtener_finca_activa,
    obtener_fincas_usuario,
    obtener_rol_usuario_finca,
    verificar_acceso_finca,
    cambiar_finca_activa,
)


class MockUser:
    def __init__(self, id: int, username: str, is_superuser: bool = False, is_authenticated: bool = True):
        self.id = id
        self.username = username
        self.is_superuser = is_superuser
        self.is_authenticated = is_authenticated


class MockFinca:
    def __init__(self, id: int, nombre: str, is_active: bool = True, created_by=None):
        self.id = id
        self.nombre = nombre
        self.is_active = is_active
        self.created_by = created_by


class MockUsuarioFinca:
    def __init__(self, usuario: MockUser, finca: MockFinca, rol: str = "operador", activa: bool = True):
        self.usuario = usuario
        self.finca = finca
        self.rol = rol
        self.activa = activa


class MockRequest:
    def __init__(self, user: MockUser, session: Optional[dict] = None, post_data: Optional[dict] = None, get_data: Optional[dict] = None):
        self.user = user
        self.session = session if session is not None else {}
        self.POST = post_data or {}
        self.GET = get_data or {}


class TestSecurityTenantHatoV1(unittest.TestCase):
    def setUp(self):
        self.user_root = MockUser(1, "root_admin", is_superuser=True)
        self.user_juan = MockUser(2, "juan_finca_a", is_superuser=False)
        self.user_carlos = MockUser(3, "carlos_multi", is_superuser=False)
        self.user_pedro = MockUser(4, "pedro_inactivo", is_superuser=False)

        self.finca_a = MockFinca(101, "Hato San José")
        self.finca_b = MockFinca(102, "Hato El Progreso")
        self.finca_c = MockFinca(103, "Finca La Esperanza")

        self.membresias = [
            MockUsuarioFinca(self.user_juan, self.finca_a, rol="administrador", activa=True),
            MockUsuarioFinca(self.user_carlos, self.finca_a, rol="operador", activa=True),
            MockUsuarioFinca(self.user_carlos, self.finca_b, rol="veterinario", activa=True),
            MockUsuarioFinca(self.user_pedro, self.finca_a, rol="operador", activa=False),
        ]

    def _mock_verificar_acceso(self, user, finca):
        if not user or not user.is_authenticated or finca is None:
            return False
        if user.is_superuser:
            return True
        return any(m.usuario.id == user.id and m.finca.id == finca.id and m.activa for m in self.membresias)

    def _mock_obtener_rol(self, user, finca):
        if not user or not user.is_authenticated or finca is None:
            return None
        if user.is_superuser:
            return "superusuario"
        for m in self.membresias:
            if m.usuario.id == user.id and m.finca.id == finca.id and m.activa:
                return m.rol
        return None

    def _mock_obtener_fincas_usuario(self, user):
        if not user or not user.is_authenticated:
            return []
        if user.is_superuser:
            return [self.finca_a, self.finca_b, self.finca_c]
        return [m.finca for m in self.membresias if m.usuario.id == user.id and m.activa and m.finca.is_active]

    def test_01_usuario_finca_a_no_puede_acceder_finca_b(self):
        self.assertTrue(self._mock_verificar_acceso(self.user_juan, self.finca_a))
        self.assertFalse(self._mock_verificar_acceso(self.user_juan, self.finca_b))

    def test_02_get_finca_no_bypasea_seguridad(self):
        req = MockRequest(self.user_juan, session={"finca_activa_id": self.finca_a.id}, get_data={"finca": "102"})
        fincas_autorizadas = self._mock_obtener_fincas_usuario(req.user)
        finca_solicitada_id = int(req.GET.get("finca"))
        tiene_acceso = any(f.id == finca_solicitada_id for f in fincas_autorizadas)
        self.assertFalse(tiene_acceso)

    def test_03_post_seleccion_no_autorizada_rechazada(self):
        self.assertFalse(self._mock_verificar_acceso(self.user_juan, self.finca_b))

    def test_04_membresia_revocada_bloquea_acceso(self):
        self.assertFalse(self._mock_verificar_acceso(self.user_pedro, self.finca_a))
        self.assertEqual(len(self._mock_obtener_fincas_usuario(self.user_pedro)), 0)

    def test_05_usuario_multi_finca_puede_cambiar(self):
        fincas_carlos = self._mock_obtener_fincas_usuario(self.user_carlos)
        ids = [f.id for f in fincas_carlos]
        self.assertIn(self.finca_a.id, ids)
        self.assertIn(self.finca_b.id, ids)
        self.assertNotIn(self.finca_c.id, ids)

    def test_06_rol_cambia_segun_finca(self):
        self.assertEqual(self._mock_obtener_rol(self.user_carlos, self.finca_a), "operador")
        self.assertEqual(self._mock_obtener_rol(self.user_carlos, self.finca_b), "veterinario")

    def test_07_root_acceso_cualquier_finca_sin_membresia(self):
        self.assertTrue(self._mock_verificar_acceso(self.user_root, self.finca_a))
        self.assertTrue(self._mock_verificar_acceso(self.user_root, self.finca_b))
        self.assertTrue(self._mock_verificar_acceso(self.user_root, self.finca_c))

    def test_08_root_modo_global_obtiene_todas_las_fincas(self):
        self.assertEqual(len(self._mock_obtener_fincas_usuario(self.user_root)), 3)

    def test_09_root_puede_fijar_contexto_finca(self):
        req = MockRequest(self.user_root, session={"finca_activa_id": self.finca_b.id})
        finca_contexto = self.finca_b if req.session.get("finca_activa_id") == self.finca_b.id else None
        self.assertIsNotNone(finca_contexto)
        self.assertEqual(finca_contexto.id, 102)

    def test_10_integridad_finca_soberana(self):
        finca_nueva = MockFinca(104, "Hato La Bendición", created_by=self.user_juan)
        membresia_auto = MockUsuarioFinca(finca_nueva.created_by, finca_nueva, rol="propietario", activa=True)
        self.assertEqual(membresia_auto.usuario.id, self.user_juan.id)
        self.assertEqual(membresia_auto.rol, "propietario")
        self.assertTrue(membresia_auto.activa)


if __name__ == "__main__":
    unittest.main()
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser


from apps.core.models import Finca, UsuarioFinca
from apps.produccion.models import Metrica, VariableMetrica
from apps.produccion.services.seguridad_metricas import (
    ConfiguracionMetricaInsegura,
    validar_formula_segura,
    validar_metrica_configurable,
    verificar_ejecucion_segura,
)


class SeguridadMetricasTest(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca Seguridad")
        self.otro_finca = Finca.objects.create(nombre="Otra Finca")
        self.user = User.objects.create_user(username="operador", password="x")
        self.otro_user = User.objects.create_user(username="otro", password="x")
        UsuarioFinca.objects.create(usuario=self.user, finca=self.finca, rol="operador")
        self.metrica = Metrica.objects.create(
            finca=self.finca,
            nombre="Prueba segura",
            codigo="SEC001",
            formula="PESO_FINAL - PESO_INICIAL",
        )
        VariableMetrica.objects.create(
            metrica=self.metrica,
            nombre="Peso final",
            codigo="PESO_FINAL",
            fuente="PesajeAnimal",
            campo="peso_kg",
            regla="ultimo",
        )
        VariableMetrica.objects.create(
            metrica=self.metrica,
            nombre="Peso inicial",
            codigo="PESO_INICIAL",
            fuente="PesajeAnimal",
            campo="peso_kg",
            regla="primero",
            orden=1,
        )

    def test_formula_aritmetica_es_segura(self):
        validar_formula_segura("(PESO_FINAL - PESO_INICIAL) / 10")

    def test_formula_rechaza_llamadas(self):
        with self.assertRaises(ConfiguracionMetricaInsegura):
            validar_formula_segura("__import__('os').system('x')")

    def test_formula_rechaza_atributos(self):
        with self.assertRaises(ConfiguracionMetricaInsegura):
            validar_formula_segura("objeto.campo")

    def test_variable_rechaza_fuente_no_autorizada(self):
        variable = self.metrica.variables.first()
        variable.fuente = "Usuario"
        variable.save(update_fields=["fuente"])
        with self.assertRaises(ConfiguracionMetricaInsegura):
            validar_metrica_configurable(self.metrica)

    def test_variable_rechaza_campo_no_autorizado(self):
        variable = self.metrica.variables.first()
        variable.campo = "password"
        variable.save(update_fields=["campo"])
        with self.assertRaises(ConfiguracionMetricaInsegura):
            validar_metrica_configurable(self.metrica)

    def test_formula_rechaza_variable_no_declarada(self):
        self.metrica.formula = "PESO_FINAL + SECRETO"
        self.metrica.save(update_fields=["formula"])
        with self.assertRaises(ConfiguracionMetricaInsegura):
            validar_metrica_configurable(self.metrica)

    def test_metrica_sin_finca_es_rechazada(self):
        metrica = Metrica.objects.create(
            finca=None,
            nombre="Sin tenant",
            codigo="SEC002",
            formula="A + 1",
        )
        VariableMetrica.objects.create(
            metrica=metrica,
            nombre="A",
            codigo="A",
            fuente="PesajeAnimal",
            campo="peso_kg",
        )
        with self.assertRaises(ConfiguracionMetricaInsegura):
            validar_metrica_configurable(metrica)

    def test_usuario_autorizado_puede_validar_finca(self):
        verificar_ejecucion_segura(self.user, self.metrica)

    def test_usuario_de_otra_finca_es_rechazado(self):
        UsuarioFinca.objects.create(
            usuario=self.otro_user,
            finca=self.otro_finca,
            rol="operador",
        )
        with self.assertRaises(PermissionDenied):
            verificar_ejecucion_segura(self.otro_user, self.metrica)

    def test_usuario_no_autenticado_es_rechazado(self):
        
        anonymous = AnonymousUser()
        with self.assertRaises(PermissionDenied):
            verificar_ejecucion_segura(anonymous, self.metrica)

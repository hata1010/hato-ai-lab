from django.contrib import admin
from django.test import SimpleTestCase

from apps.ganado.models_reproduccion import (
    ControlLeche,
    CriaNacimiento,
    EventoReproductivo,
    Lactancia,
)


class CapturaReproduccionLactanciaAdminTests(SimpleTestCase):
    """Verifica que las entidades nuevas estén disponibles para captura en Admin."""

    def test_eventos_reproductivos_estan_registrados(self):
        self.assertIn(EventoReproductivo, admin.site._registry)
        model_admin = admin.site._registry[EventoReproductivo]
        self.assertIn("animal__numero_arete", model_admin.search_fields)
        self.assertIn("toro__numero_arete", model_admin.search_fields)
        self.assertIn("semen_codigo", model_admin.search_fields)

    def test_crias_nacimiento_estan_registradas(self):
        self.assertIn(CriaNacimiento, admin.site._registry)
        model_admin = admin.site._registry[CriaNacimiento]
        self.assertIn("parto__animal__numero_arete", model_admin.search_fields)
        self.assertIn("animal__numero_arete", model_admin.search_fields)

    def test_lactancias_estan_registradas(self):
        self.assertIn(Lactancia, admin.site._registry)
        model_admin = admin.site._registry[Lactancia]
        self.assertIn("animal__numero_arete", model_admin.search_fields)
        self.assertIn("parto_origen", model_admin.autocomplete_fields)

    def test_controles_lecheros_estan_registrados(self):
        self.assertIn(ControlLeche, admin.site._registry)
        model_admin = admin.site._registry[ControlLeche]
        self.assertIn("lactancia__animal__numero_arete", model_admin.search_fields)
        self.assertIn("lactancia", model_admin.autocomplete_fields)

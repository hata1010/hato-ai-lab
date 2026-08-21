from django.apps import AppConfig


class GanadoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ganado'

    def ready(self):
        # Registra los modelos zootécnicos adicionales sin duplicar
        # la definición existente de apps.ganado.models.
        from . import models_reproduccion  # noqa: F401
        from . import admin_reproduccion  # noqa: F401

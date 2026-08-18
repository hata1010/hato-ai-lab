from django.urls import path

from .views import (
    dashboard,
    indicadores,
    prueba_motor,
)


urlpatterns = [

    path(
        "",
        dashboard,
        name="dashboard",
    ),

    path(
        "indicadores/",
        indicadores,
        name="indicadores",
    ),

    path(
        "prueba-motor/",
        prueba_motor,
        name="prueba_motor",
    ),
]
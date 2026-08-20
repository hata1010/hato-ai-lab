# app/config/urls.py

from django.contrib import admin
from django.urls import include, path
from apps.core import views as core_views
from apps.administrador import views as admin_views


urlpatterns = [
    # HOME / PORTAL PRINCIPAL DEL SISTEMA
    path("", admin_views.dashboard, name="home"),

    # ADMINISTRACIÓN DJANGO
    path("admin/", admin.site.urls),

    # CONTROL MULTI-FINCA
    path(
        "finca/seleccionar/",
        core_views.seleccionar_finca,
        name="seleccionar_finca",
    ),
    path(
        "finca/<int:finca_id>/mapa/",
        core_views.mapa_finca,
        name="mapa_finca",
    ),
    path(
        "ganado/animales/potrero/<int:potrero_id>/",
        core_views.animales_por_potrero,
        name="animales_por_potrero",
    ),

    # MÓDULOS DE APLICACIONES
    path("administrador/", include("apps.administrador.urls")),
    path("produccion/", include("apps.produccion.urls")),
]

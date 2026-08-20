# app/config/urls.py

from django.contrib import admin
from django.urls import include, path
from apps.core import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "finca/seleccionar/",
        views.seleccionar_finca,
        name="seleccionar_finca",
    ),

    path(
        "finca/<int:finca_id>/mapa/",
        views.mapa_finca,
        name="mapa_finca",
    ),

    path(
        "ganado/animales/potrero/<int:potrero_id>/",
        views.animales_por_potrero,
        name="animales_por_potrero",
    ),

    path(
        "administrador/",
        include("apps.administrador.urls"),
    ),

    path(
        "produccion/",
        include("apps.produccion.urls"),
    ),
]
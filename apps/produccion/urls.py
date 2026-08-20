from django.urls import path
from . import views

app_name = "produccion"

urlpatterns = [
    # Vistas existentes conservadas
    path("", views.dashboard, name="dashboard"),
    path("indicadores/", views.indicadores, name="indicadores"),
    path("prueba-motor/", views.prueba_motor, name="prueba_motor"),

    # Rutas oficiales de la Página de Definición y Administración de Métricas V1
    path("metricas/", views.lista_metricas, name="lista_metricas"),
    path("metricas/crear/", views.crear_editar_metrica, name="crear_metrica"),
    path("metricas/<int:metrica_id>/editar/", views.crear_editar_metrica, name="editar_metrica"),
    path("metricas/probar/", views.probar_metrica, name="probar_metrica_general"),
    path("metricas/<int:metrica_id>/probar/", views.probar_metrica, name="probar_metrica"),
    path("metricas/<int:metrica_id>/toggle-activa/", views.toggle_metrica_activa, name="toggle_activa"),
]

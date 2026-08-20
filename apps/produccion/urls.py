from django.urls import path
from . import views

app_name = "produccion"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("indicadores/", views.indicadores, name="indicadores"),
    path("prueba-motor/", views.prueba_motor, name="prueba_motor"),
    path("metricas/", views.lista_metricas, name="lista_metricas"),
    path("metricas/crear/", views.crear_editar_metrica, name="crear_metrica"),
    path("metricas/<int:metrica_id>/editar/", views.crear_editar_metrica, name="editar_metrica"),
    path("metricas/probar/", views.probar_metrica, name="probar_metrica_general"),
    path("metricas/<int:metrica_id>/probar/", views.probar_metrica, name="probar_metrica"),
    path("metricas/<int:metrica_id>/toggle-activa/", views.toggle_metrica_activa, name="toggle_activa"),
    path("metricas-globales/", views.metricas_globales_lista, name="metricas_globales_lista"),
    path("metricas-globales/crear/", views.crear_editar_metrica_global, name="crear_metrica_global"),
    path("metricas-globales/<int:metrica_id>/editar/", views.crear_editar_metrica_global, name="editar_metrica_global"),
    path("metricas-globales/<int:metrica_id>/contraste/", views.contraste_global_metrica, name="contraste_global"),
    path("metricas-globales/<int:metrica_id>/toggle/", views.toggle_metrica_global, name="toggle_metrica_global"),
]

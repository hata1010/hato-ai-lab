from django.urls import path

from . import salud_views
from . import views

app_name = "ganado"

urlpatterns = [
    path("animales/", views.lista_animales, name="lista_animales"),
    path("animales/crear/", views.crear_animal, name="crear_animal"),
    path("animales/<int:animal_id>/", views.detalle_animal, name="detalle_animal"),
    path("animales/<int:animal_id>/editar/", views.editar_animal, name="editar_animal"),
    path("salud/", salud_views.lista_salud, name="lista_salud"),
    path("salud/animal/<int:animal_id>/", salud_views.historia_salud_animal, name="historia_salud_animal"),
    path("salud/crear/", salud_views.crear_evento_salud, name="crear_evento_salud"),
    path("salud/<int:evento_id>/editar/", salud_views.editar_evento_salud, name="editar_evento_salud"),
]

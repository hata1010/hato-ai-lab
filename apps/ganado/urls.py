from django.urls import path

from . import views

app_name = "ganado"

urlpatterns = [
    path("animales/", views.lista_animales, name="lista_animales"),
    path("animales/crear/", views.crear_animal, name="crear_animal"),
    path("animales/<int:animal_id>/", views.detalle_animal, name="detalle_animal"),
    path("animales/<int:animal_id>/editar/", views.editar_animal, name="editar_animal"),
]

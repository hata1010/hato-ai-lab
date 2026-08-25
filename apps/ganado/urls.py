from django.urls import path

from . import movilidad_views
from . import pesaje_views
from . import salud_views
from . import views

app_name = "ganado"

urlpatterns = [
    path("animales/", views.lista_animales, name="lista_animales"),
    path("animales/crear/", views.crear_animal, name="crear_animal"),
    path("animales/<int:animal_id>/", views.detalle_animal, name="detalle_animal"),
    path("animales/<int:animal_id>/editar/", views.editar_animal, name="editar_animal"),
    path("movilidad/", movilidad_views.lista_movilidad, name="lista_movilidad"),
    path("movilidad/crear/", movilidad_views.crear_movimiento, name="crear_movimiento"),
    path("movilidad/animal/<int:animal_id>/", movilidad_views.historial_movilidad_animal, name="historial_movilidad_animal"),
    path("movilidad/<int:movimiento_id>/cambiar-potrero/", movilidad_views.cambiar_potrero, name="cambiar_potrero"),
    path("movilidad/<int:movimiento_id>/cerrar/", movilidad_views.cerrar_movimiento, name="cerrar_movimiento"),
    path("pesajes/", pesaje_views.lista_pesajes, name="lista_pesajes"),
    path("pesajes/crear/", pesaje_views.crear_pesaje, name="crear_pesaje"),
    path("pesajes/animal/<int:animal_id>/", pesaje_views.historial_pesajes_animal, name="historial_pesajes_animal"),
    path("salud/", salud_views.lista_salud, name="lista_salud"),
    path("salud/animal/<int:animal_id>/", salud_views.historia_salud_animal, name="historia_salud_animal"),
    path("salud/crear/", salud_views.crear_evento_salud, name="crear_evento_salud"),
    path("salud/<int:evento_id>/editar/", salud_views.editar_evento_salud, name="editar_evento_salud"),
]

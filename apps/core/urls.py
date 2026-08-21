from django.urls import path

from . import potrero_views

app_name = "potreros"

urlpatterns = [
    path("", potrero_views.lista_potreros, name="lista"),
    path("crear/", potrero_views.crear_potrero, name="crear"),
    path("<int:potrero_id>/", potrero_views.detalle_potrero, name="detalle"),
    path("<int:potrero_id>/editar/", potrero_views.editar_potrero, name="editar"),
    path("<int:potrero_id>/eliminar/", potrero_views.eliminar_potrero, name="eliminar"),
]

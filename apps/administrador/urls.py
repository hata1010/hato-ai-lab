from django.urls import path
from . import views, compras_views

app_name = "administrador"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("indicadores/", views.indicadores, name="indicadores"),
    path("compras-adquisiciones/", compras_views.compras_adquisiciones, name="compras_adquisiciones"),
]

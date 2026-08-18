from django.urls import path
from . import views

app_name = "administrador"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("indicadores/", views.indicadores, name="indicadores"),
]
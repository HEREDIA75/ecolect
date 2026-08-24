from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("mapa/", views.mapa_ecopontos, name="mapa"),  # <-- Adicione esta linha
]

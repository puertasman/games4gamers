from django.urls import path
from .views import (home,
                    juegos_principal)

from .views import juego_detalle

urlpatterns = [
    path('', home, name="home"),
    path('juegos/', juegos_principal, name="juegos_principal"),
    path('juegos/<int:juego_id>/', juego_detalle, name='juego_detalle'),
]
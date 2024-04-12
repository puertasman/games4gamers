from django.urls import path
from .views import (home,
                    juegos_principal)

urlpatterns = [
    path('', home, name="home"),
    path('juegos/', juegos_principal, name="juegos_principal"),
]
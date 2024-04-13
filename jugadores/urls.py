from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (jugadores_registro,
                    jugadores_principal,
                    jugadores_login,
                    jugador_info,
                    jugadores_logout,
                    inscribir_juego,
                    )

urlpatterns = [
    path('jugadores/', jugadores_principal, name="jugadores_principal"),
    path('jugadores/registro', jugadores_registro, name="jugadores_registro"),
    path('jugadores/login', jugadores_login, name="jugadores_login"),
    path('jugadores/jugador/<int:id>', jugador_info, name="jugador_info"),
    path('jugadores/cerrar_sesion', jugadores_logout, name='logout'),
    path('inscribir-juego/<int:juego_id>/', inscribir_juego, name='inscribir-juego'),
]

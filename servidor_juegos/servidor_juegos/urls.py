from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("jugadores.urls")), # mejor tenerlas por separado
    path('', include("juegos.urls")),
    path('', include("torneos.urls")),
]

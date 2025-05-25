from django.urls import path
from . import views # Ensure views is imported

urlpatterns = [
    path('torneos/', views.torneos_principal, name="torneos_principal"),
    path('torneos/<int:torneo_id>/', views.torneo_detalle, name='torneo_detalle'),
    path('torneos/<int:torneo_id>/inscribir/', views.inscribir_torneo, name='inscribir_torneo'),
]
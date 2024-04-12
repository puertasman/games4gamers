from django.urls import path
from .views import (torneos_principal)

urlpatterns = [
    path('torneos/', torneos_principal, name="torneos_principal"),
]
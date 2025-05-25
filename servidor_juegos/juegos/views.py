from django.shortcuts import render, get_object_or_404
from .models import Juego

def juegos_principal(request):
    juegos = Juego.objects.all()
    return render(request, 'juegos/juegos_principal.html', {'juegos': juegos})

def juego_detalle(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id)
    return render(request, 'juegos/juego_detalle.html', {'juego': juego})

def home(request):
    return render(request, 'home.html')
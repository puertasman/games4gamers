from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Torneo, InscripcionTorneo
from jugadores.models import Jugadores

def torneos_principal(request):
    torneos = Torneo.objects.all().order_by('-fecha_inicio')
    return render(request, 'torneos/torneos_principal.html', {'torneos': torneos})

def torneo_detalle(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    inscripciones = torneo.inscripciones.all().select_related('jugador__nombre') # Fetches related User's username

    usuario_registrado = False
    if request.user.is_authenticated:
        jugador_actual = Jugadores.objects.filter(nombre=request.user).first()
        if jugador_actual:
            usuario_registrado = InscripcionTorneo.objects.filter(torneo=torneo, jugador=jugador_actual).exists()

    return render(request, 'torneos/torneo_detalle.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
        'usuario_registrado': usuario_registrado
    })

@login_required
def inscribir_torneo(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    try:
        jugador_profile = get_object_or_404(Jugadores, nombre=request.user)
    except Jugadores.DoesNotExist: # This specific exception might not be needed if get_object_or_404 handles it
        messages.error(request, "No se encontró un perfil de jugador asociado a tu usuario.")
        return redirect('torneo_detalle', torneo_id=torneo.id)

    # Validation Checks
    if torneo.estado not in ['PROXIMAMENTE', 'ACTIVO']:
        messages.error(request, "Este torneo no está abierto para inscripciones.")
        return redirect('torneo_detalle', torneo_id=torneo.id)

    if torneo.max_participantes != 0 and torneo.inscripciones.count() >= torneo.max_participantes:
        messages.error(request, "El torneo ya está lleno.")
        return redirect('torneo_detalle', torneo_id=torneo.id)

    if InscripcionTorneo.objects.filter(torneo=torneo, jugador=jugador_profile).exists():
        messages.error(request, "Ya estás inscrito en este torneo.")
        return redirect('torneo_detalle', torneo_id=torneo.id)

    # Create InscripcionTorneo
    InscripcionTorneo.objects.create(torneo=torneo, jugador=jugador_profile)
    messages.success(request, "¡Inscripción exitosa!")
    return redirect('torneo_detalle', torneo_id=torneo.id)
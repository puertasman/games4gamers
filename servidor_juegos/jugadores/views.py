from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import formulario_registro_usuarios

from .models import Participaciones, Jugadores
from juegos.models import Juego


def jugadores_principal(request):
    juegos = Juego.objects.all()
    mejores_por_juego = {}
    for juego in juegos:
        participaciones = None
        if juego.id == 1: # Hard Run
            try:
                participaciones = Participaciones.objects.filter(juego=juego).order_by('detalles__tiempo_total')[:3]
            except Exception as e:
                print(f"Error ordering Hard Run: {e}")
                participaciones = Participaciones.objects.filter(juego=juego)[:3]
        elif juego.id == 2: # Seek and hit
            try:
                # Attempt to order by puntos descending. Note: JSON field ordering might be tricky.
                participaciones = Participaciones.objects.filter(juego=juego).order_by('-detalles__puntos')[:3]
            except Exception as e:
                print(f"Error ordering Seek and hit by puntos: {e}")
                # Fallback if ordering by JSON field fails
                participaciones = Participaciones.objects.filter(juego=juego)[:3]
        elif juego.id == 3: # Bastions of Dusk
            try:
                # Attempt to order by pantalla descending.
                participaciones = Participaciones.objects.filter(juego=juego).order_by('-detalles__pantalla')[:3]
            except Exception as e:
                print(f"Error ordering Bastions of Dusk by pantalla: {e}")
                participaciones = Participaciones.objects.filter(juego=juego)[:3]
        else: # For other games
            participaciones = Participaciones.objects.filter(juego=juego)[:3]
        
        mejores_por_juego[juego] = participaciones
        
    context = {'mejores_por_juego': mejores_por_juego}
    return render(request, 'jugadores/jugadores_principal.html', context)

def jugador_info(request, id):
    user = get_object_or_404(User, id=id)
    jugador_profile = get_object_or_404(Jugadores, nombre=user)
    juegos = Juego.objects.all()
    
    juegos_participaciones_data = []
    for juego in juegos:
        participacion = Participaciones.objects.filter(jugador=jugador_profile, juego=juego).first()
        juegos_participaciones_data.append({
            'juego': juego,
            'participacion': participacion
        })

    return render(request, 'jugadores/jugador.html', {
        'jugador_user': user, # Renamed from 'user' to 'jugador_user' for clarity
        'jugador_profile': jugador_profile,
        'juegos_participaciones_data': juegos_participaciones_data,
    })

def jugadores_registro(request):
    if request.user.is_authenticated:
        return redirect('jugador_info', request.user.id)
        # si ya está dentro no necesita hacer login y lo mando a la página de usuario
    if request.method == 'POST':
        formulario = formulario_registro_usuarios(request.POST)  # cogemos los datos del formulario
        if formulario.is_valid():  # si los datos son válidos
            user = formulario.save()  # guardamos los datos
            nivel = formulario.cleaned_data.get('nivel')
            # creo el jugador con su nivel
            Jugadores.objects.create(nombre=user, nivel=nivel)
            login(request, user)  # iniciamos sesión
            return redirect('jugador_info', id=user.id)
            # lo envío a la página del usuario

        else:
            for error in list(formulario.errors.values()):
                print(request,error)  # comprobar errores y arreglar lo que se pide

    else:
        formulario = formulario_registro_usuarios()

    return render(request, 'jugadores/jugadores_registro.html', {'formulario': formulario})

def jugadores_login(request):
    if request.user.is_authenticated:
        print("ya está logueado")
        print(request.user.id)

        return redirect('jugador_info', request.user.id)
        # si ya está dentro no se puede registrar y lo mando fuera
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print("enviado")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('jugador_info', id=user.id)
                # Redireccionar a la web con la info del usuario
        else:
            print(form.errors)  # Agrega esto para depurar y ver los errores del formulario


    else:
        form = AuthenticationForm()
    return render(request, 'jugadores/jugadores_login.html', {'form': form})


def jugadores_logout(request):
    logout(request)
    return redirect('jugadores_principal')

# para registrar una participación de un jugador
@login_required
def inscribir_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    jugador = get_object_or_404(Jugadores, nombre=request.user)

    detalles_default = {}
    if juego.id == 1: # Hard Run
        detalles_default = {"circuitos": 0, "tiempo_total": "00:00:00"}
    elif juego.id == 2: # Seek and hit
        detalles_default = {"kills": 0, "killed": 0, "nivel": 0, "puntos": 0}
    elif juego.id == 3: # Bastions of Dusk
        detalles_default = {"nivel": 0, "pantalla": "1.1"}
    # For any other game, detalles_default remains {}

    participacion, created = Participaciones.objects.get_or_create(
        jugador=jugador,
        juego=juego,
        defaults={'detalles': detalles_default}
    )

    return redirect('jugador_info', request.user.id)
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
        # Aquí asumimos que hay algún campo `puntaje` o similar para determinar el "mejor"
        # Ajuste este query según su modelo y lógica de negocio
        mejores = Participaciones.objects.filter(juego=juego)[:3]  # sólo los 3 mejores
        mejores_por_juego[juego.nombre] = mejores
    context = {'mejores_por_juego': mejores_por_juego}
    return render(request, 'jugadores/jugadores_principal.html', context)

def jugador_info(request,id):
    # pedimos el objeto a la base de datos
    user = get_object_or_404(User, id=id)  # Si no lo encuentra envía a la página 404
    # retornamos una http con la plantilla jugador.html y el objeto de la base de datos
    juegos = Juego.objects.all()
    jugador = Jugadores.objects.get(nombre=request.user)
    # creo una lista con la información del juego para el jugador
    datos_especificos_del_juego = {
        1: {'nombre': 'Hard Run', 'detalles': 'Detalles del Juego 1', 'otra_info': 'Más info del Juego 1'},
    }

        # Añade un diccionario con la información del juego y los detalles de la participación
        juegos_y_participaciones.append({
            'juego': juego,
            'detalles': detalles,
        })

    return render(request, 'jugadores/jugador.html', {
        'user': user,
        'juegos_y_participaciones': juegos_y_participaciones,
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
    if juego.id == 1:
        detalles_default = {"circuitos": 0}
    elif juego.id == 2:
        detalles_default = {"kills": 0, "killed": 0, "nivel": 0, "puntos": 0}
    elif juego.id == 3:
        detalles_default = {"nivel": 0, "pantalla": "1.1"}

    participacion, created = Participaciones.objects.get_or_create(
        jugador=jugador,
        juego=juego,
        defaults={'detalles': detalles_default}
    )

    return redirect('jugador_info', request.user.id)
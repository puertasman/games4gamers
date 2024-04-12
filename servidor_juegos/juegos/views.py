from django.shortcuts import render

def juegos_principal(request):
    return render(request, 'juegos/juegos_principal.html')

def home(request):
    return render(request, 'home.html')
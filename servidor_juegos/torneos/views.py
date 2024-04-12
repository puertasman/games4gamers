from django.shortcuts import render

def torneos_principal(request):
    return render(request, 'torneos/torneos_principal.html')
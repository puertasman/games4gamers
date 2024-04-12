from django.contrib import admin

from .models import Jugadores, Participaciones

class AdminDBs(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'nivel',
    )

admin.site.register(Jugadores, AdminDBs)
admin.site.register(Participaciones)
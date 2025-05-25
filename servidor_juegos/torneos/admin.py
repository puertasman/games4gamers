from django.contrib import admin
from .models import Torneo, InscripcionTorneo

class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'juego', 'fecha_inicio', 'fecha_fin', 'estado', 'max_participantes')
    list_filter = ('estado', 'juego')
    search_fields = ('nombre', 'juego__nombre')

class InscripcionTorneoAdmin(admin.ModelAdmin):
    list_display = ('torneo', 'jugador', 'fecha_inscripcion')
    list_filter = ('torneo__juego', 'torneo__estado')
    search_fields = ('torneo__nombre', 'jugador__nombre__username')

admin.site.register(Torneo, TorneoAdmin)
admin.site.register(InscripcionTorneo, InscripcionTorneoAdmin)
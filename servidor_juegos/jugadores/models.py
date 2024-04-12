from django.db import models
from django.conf import settings
from juegos.models import Juego
# Traigo la base de datos de Juego para poder coger la id del juego

class Jugadores(models.Model):
    # niveles para hacer un campo con opcion de selección
    NIVEL_OPCIONES = [
        ('AMATEUR', 'Amateur'),
        ('NORMAL', 'Normal'),
        ('EXPERT', 'Expert'),
    ]
    # no hace falta crear id porque django lo hace automáticamente
    # no hace falta añadir not null porque django lo hace for defecto
    nombre = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=7, choices=NIVEL_OPCIONES, default='AMATEUR')

    class Meta:
        # clase para evitar que pong el plural con 2 s en la base de datos
        verbose_name_plural = "Jugadores"


    def __str__(self):
        return str(self.nombre)

class Participaciones(models.Model):
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    detalles = models.JSONField(null=True)
    # coge las claves primarias de jugadores y juego
    if juego == 1:
        detalles = models.JSONField(default=lambda: {"nivel": 0, "pantalla": "1.1"})
    elif juego == 2:
        detalles = models.JSONField(default=lambda: {})
    elif juego == 3:
        detalles = models.JSONField(default=lambda: {"kills": 0, "killed": 0, "nivel": 0, "puntos": 0})
    # nivel y pantalla por defecto

    class Meta:
    # clase para evitar que pong el plural con 2 s en la base de datos
        verbose_name_plural = "Participaciones"

    def __str__(self):
        return f"{self.jugador.nombre} - {self.juego.nombre}"

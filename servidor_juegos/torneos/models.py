from django.db import models
from juegos.models import Juego
from jugadores.models import Jugadores

class Torneo(models.Model):
    ESTADO_CHOICES = [
        ('PROXIMAMENTE', 'Próximamente'),
        ('ACTIVO', 'Activo'),
        ('FINALIZADO', 'Finalizado'),
    ]

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='torneos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='PROXIMAMENTE')
    max_participantes = models.PositiveIntegerField(default=0)  # 0 for unlimited

    def __str__(self):
        return self.nombre

class InscripcionTorneo(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='inscripciones')
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE, related_name='inscripciones_torneo')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    # ESTADO_INSCRIPCION_CHOICES could be added here if complex logic for waitlists/cancellations is needed.
    # For now, keeping it simple.

    class Meta:
        unique_together = ('torneo', 'jugador')

    def __str__(self):
        return f"{self.jugador.nombre} inscrito en {self.torneo.nombre}"

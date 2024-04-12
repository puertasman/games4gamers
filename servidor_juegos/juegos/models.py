from django.db import models

class Juego(models.Model):
    # no hace falta crear id porque django lo hace automáticamente
    # no hace falta añadir not null porque django lo hace for defecto
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=100,default='empty')
    descripcion = models.TextField()
    fecha_de_lanzamiento = models.DateField()
    genero = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
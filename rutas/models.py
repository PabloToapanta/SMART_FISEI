# apps/rutas/models.py

from django.db import models

class EspacioFisico(models.Model):
    TIPO_CHOICES = [
        ('aula', 'Aula'),
        ('laboratorio', 'Laboratorio'),
        ('oficina', 'Oficina'),
        ('bloque', 'Bloque'),
        ('pasillo', 'Pasillo'),
        ('entrada', 'Entrada'),
    ]
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)   # Ej: FISEI-B2-L3
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    bloque = models.CharField(max_length=10, blank=True)    # A, B, C...
    piso = models.IntegerField(default=1)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"


class ConexionEspacio(models.Model):
    origen = models.ForeignKey(EspacioFisico, on_delete=models.CASCADE, related_name='conexiones_salida')
    destino = models.ForeignKey(EspacioFisico, on_delete=models.CASCADE, related_name='conexiones_entrada')
    peso = models.FloatField(default=1.0)       # distancia o tiempo estimado
    descripcion = models.CharField(max_length=200, blank=True)
    bidireccional = models.BooleanField(default=True)

    class Meta:
        unique_together = ('origen', 'destino')

    def __str__(self):
        return f"{self.origen.codigo} → {self.destino.codigo} (peso: {self.peso})"
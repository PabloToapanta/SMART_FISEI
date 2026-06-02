# apps/historial/models.py

from django.db import models
from usuarios.models import Usuario

class HistorialAccion(models.Model):
    MODULO_CHOICES = [
        ('turnos', 'Turnos'),
        ('tramites', 'Trámites'),
        ('documentos', 'Documentos'),
        ('rutas', 'Rutas'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial')
    modulo = models.CharField(max_length=20, choices=MODULO_CHOICES)
    accion = models.CharField(max_length=200)
    detalle = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.usuario} — {self.modulo}: {self.accion}"
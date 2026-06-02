# apps/tramites/models.py

from django.db import models
from usuarios.models import Usuario

class TipoTramite(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    requiere_documentos = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Tramite(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('archivado', 'Archivado'),
    ]
    codigo = models.CharField(max_length=15, unique=True)   # Ej: TR-2026-001
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tramites')
    tipo = models.ForeignKey(TipoTramite, on_delete=models.PROTECT)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.codigo} — {self.tipo} [{self.get_estado_display()}]"


class HistorialEstadoTramite(models.Model):
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=20, choices=Tramite.ESTADO_CHOICES, blank=True)
    estado_nuevo = models.CharField(max_length=20, choices=Tramite.ESTADO_CHOICES)
    responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ['fecha']
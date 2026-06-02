# apps/turnos/models.py

from django.db import models
from usuarios.models import Usuario

class Ventanilla(models.Model):
    nombre = models.CharField(max_length=50)          # Ej: "Ventanilla 1"
    descripcion = models.CharField(max_length=200, blank=True)
    activa = models.BooleanField(default=True)
    responsable = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'rol': 'administrativo'}
    )

    def __str__(self):
        return self.nombre


class Turno(models.Model):
    ESTADO_CHOICES = [
        ('espera', 'En Espera'),
        ('llamado', 'Llamado'),
        ('en_atencion', 'En Atención'),
        ('atendido', 'Atendido'),
        ('cancelado', 'Cancelado'),
    ]
    MOTIVO_CHOICES = [
        ('tramite', 'Trámite'),
        ('consulta', 'Consulta'),
        ('documento', 'Documento'),
    ]
    codigo = models.CharField(max_length=10, unique=True)   # Ej: T-0042
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='turnos')
    ventanilla = models.ForeignKey(Ventanilla, on_delete=models.SET_NULL, null=True, blank=True)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='espera')
    hora_solicitud = models.DateTimeField(auto_now_add=True)
    hora_inicio_atencion = models.DateTimeField(null=True, blank=True)
    hora_fin_atencion = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['hora_solicitud']

    def __str__(self):
        return f"{self.codigo} — {self.usuario} [{self.get_estado_display()}]"
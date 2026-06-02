# apps/documentos/models.py

from django.db import models
from usuarios.models import Usuario

class NodoJerarquico(models.Model):
    TIPO_CHOICES = [
        ('facultad', 'Facultad'),
        ('departamento', 'Departamento'),
        ('carrera', 'Carrera'),
        ('area', 'Área'),
    ]
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    padre = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='hijos'
    )
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.nombre}"


class Documento(models.Model):
    nombre = models.CharField(max_length=200)
    nodo = models.ForeignKey(NodoJerarquico, on_delete=models.CASCADE, related_name='documentos')
    archivo = models.FileField(upload_to='documentos/%Y/%m/', null=True, blank=True)
    url_externo = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)
    subido_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
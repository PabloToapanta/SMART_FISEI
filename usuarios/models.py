from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('administrativo', 'Personal Administrativo'),
        ('docente', 'Docente'),
        ('estudiante', 'Estudiante'),
    ]
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='estudiante')
    cedula = models.CharField(max_length=10, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'rol']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"
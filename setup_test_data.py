import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from tramites.models import TipoTramite
from turnos.models import Ventanilla
from documentos.models import NodoJerarquico

def setup():
    print("=== Iniciando configuración de datos de prueba ===")

    # 1. Usuarios
    usuarios_data = [
        ('admin@fisei.uta.edu.ec', 'Admin Sistema', 'admin'),
        ('administrativo@fisei.uta.edu.ec', 'María Secretaria', 'administrativo'),
        ('docente@fisei.uta.edu.ec', 'Dr. Carlos Pérez', 'docente'),
        ('estudiante1@fisei.uta.edu.ec', 'Ana Torres', 'estudiante'),
        ('estudiante2@fisei.uta.edu.ec', 'Luis Mora', 'estudiante'),
    ]

    for email, nombre, rol in usuarios_data:
        user, created = Usuario.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                'first_name': nombre.split(' ')[0],
                'last_name': ' '.join(nombre.split(' ')[1:]),
                'rol': rol,
                'is_staff': (rol == 'admin'),
                'is_superuser': (rol == 'admin'),
            }
        )
        if created:
            user.set_password('Admin2026#')
            user.save()
            print(f"Usuario creado: {email} ({rol})")
        else:
            print(f"Usuario ya existe: {email}")

    # 2. Tipos de Trámite
    if TipoTramite.objects.count() == 0:
        tipos = [
            "Certificado de matrícula", "Récord académico", "Permiso de ausencia",
            "Solicitud de beca", "Cambio de carrera", "Certificado de egresamiento",
            "Homologación de materias", "Retiro de materia"
        ]
        for t in tipos:
            TipoTramite.objects.create(nombre=t, activo=True)
        print(f"Creados {len(tipos)} tipos de trámite.")
    else:
        print("Tipos de trámite ya existen.")

    # 3. Ventanillas
    if Ventanilla.objects.count() == 0:
        admin_user = Usuario.objects.filter(rol='administrativo').first()
        ventanillas = ["Ventanilla 1", "Ventanilla 2", "Ventanilla 3"]
        for v in ventanillas:
            Ventanilla.objects.create(nombre=v, responsable=admin_user, activa=True)
        print(f"Creadas {len(ventanillas)} ventanillas.")
    else:
        print("Ventanillas ya existen.")

    # 4. Nodo Raíz
    if not NodoJerarquico.objects.filter(nombre="FISEI").exists():
        NodoJerarquico.objects.create(nombre="FISEI", tipo='facultad', padre=None)
        print("Nodo raíz FISEI creado.")
    else:
        print("Nodo raíz ya existe.")

    print("=== Configuración finalizada con éxito ===")

if __name__ == "__main__":
    setup()

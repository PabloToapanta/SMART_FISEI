import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from usuarios.models import Usuario
from turnos.models import Ventanilla, Turno
from tramites.models import TipoTramite, Tramite
from documentos.models import NodoJerarquico, Documento
from rutas.models import EspacioFisico, ConexionEspacio
from historial.models import HistorialAccion

def cargar_todo():
    print("=== INICIANDO CARGA MASIVA DE DATOS SMARTFISEI (COMPLETO) ===")

    # 1. Limpiar datos previos
    print("Vaciando tablas existentes...")
    HistorialAccion.objects.all().delete()
    ConexionEspacio.objects.all().delete()
    EspacioFisico.objects.all().delete()
    Documento.objects.all().delete()
    NodoJerarquico.objects.all().delete()
    Turno.objects.all().delete()
    Tramite.objects.all().delete()
    Ventanilla.objects.all().delete()
    TipoTramite.objects.all().delete()
    Usuario.objects.all().delete()

    # 2. Crear Usuarios
    print("Creando usuarios institucionales...")
    usuarios = [
        ('admin@uta.edu.ec', 'Admin Sistema', 'admin'),
        ('administrativo@uta.edu.ec', 'María Secretaria', 'administrativo'),
        ('docente@uta.edu.ec', 'Dr. Carlos Pérez', 'docente'),
        ('estudiante1@uta.edu.ec', 'Ana Torres', 'estudiante'),
        ('estudiante2@uta.edu.ec', 'Luis Mora', 'estudiante'),
    ]
    user_objs = {}
    for email, nombre, rol in usuarios:
        user = Usuario.objects.create_user(
            username=email.split('@')[0],
            email=email,
            password='Admin2026#',
            first_name=nombre.split(' ')[0],
            last_name=' '.join(nombre.split(' ')[1:]),
            rol=rol,
            is_staff=(rol in ['admin', 'administrativo']),
            is_superuser=(rol == 'admin')
        )
        user_objs[rol] = user
        print(f"  - {rol}: {email}")

    # 3. Crear Catálogo de Trámites (15 tipos)
    print("Cargando catálogo de trámites...")
    tramites_data = [
        ("Certificado de matrícula", "Constancia oficial del período académico vigente", False),
        ("Récord académico", "Historial completo de calificaciones por asignatura", False),
        ("Certificado de egresamiento", "Constancia de haber aprobado todas las materias", False),
        ("Certificado de no adeudar", "Constancia de no tener deudas con la facultad", False),
        ("Permiso de ausencia", "Justificación oficial de inasistencias a clases", True),
        ("Solicitud de beca", "Postulación a programas de ayuda económica", True),
        ("Cambio de carrera", "Transferencia interna entre carreras de la FISEI", True),
        ("Homologación de materias", "Reconocimiento de asignaturas aprobadas en otra institución", True),
        ("Retiro de materia", "Solicitud formal de baja de una asignatura", True),
        ("Segunda matrícula", "Autorización para matricularse por segunda ocasión en una materia", True),
        ("Tercera matrícula", "Solicitud de matrícula extraordinaria con aval del consejo", True),
        ("Revisión de examen", "Impugnación formal de calificación obtenida", True),
        ("Constancia de horario", "Documento con el horario oficial del estudiante", False),
        ("Solicitud de práctica preprofesional", "Registro de inicio de horas prácticas externas", True),
        ("Titulación — tema de proyecto", "Aprobación del tema de trabajo de titulación", True),
    ]
    for nombre, desc, req in tramites_data:
        TipoTramite.objects.create(nombre=nombre, descripcion=desc, requiere_documentos=req)
    print(f"  - {len(tramites_data)} tipos de trámites registrados.")

    # 4. Crear Ventanillas
    print("Configurando ventanillas...")
    Ventanilla.objects.create(nombre="Ventanilla 1", responsable=user_objs['administrativo'], activa=True)
    Ventanilla.objects.create(nombre="Ventanilla 2", responsable=user_objs['administrativo'], activa=True)
    Ventanilla.objects.create(nombre="Ventanilla 3", responsable=user_objs['admin'], activa=True)
    print("  - 3 ventanillas activas creadas.")

    # 5. Jerarquía Documental (Árbol N-ario)
    print("Construyendo jerarquía institucional (Árbol N-ario)...")
    fisei = NodoJerarquico.objects.create(nombre="FISEI — Facultad de Ingeniería en Sistemas, Electrónica e Industrial", tipo='facultad')
    
    # Bloque Secretaría
    sec = NodoJerarquico.objects.create(nombre="Secretaría General", tipo='departamento', padre=fisei)
    reg = NodoJerarquico.objects.create(nombre="Reglamentos y Normativas", tipo='area', padre=sec)
    for d in ["reglamento_interno_fisei.pdf", "reglamento_practicas.pdf", "codigo_etica.pdf"]:
        Documento.objects.create(nombre=d, nodo=reg)
        
    form = NodoJerarquico.objects.create(nombre="Formularios Oficiales", tipo='area', padre=sec)
    for d in ["form_matricula.docx", "form_retiro.docx", "form_beca.docx"]:
        Documento.objects.create(nombre=d, nodo=form)

    # Carreras
    sw = NodoJerarquico.objects.create(nombre="Carrera de Ingeniería en Software", tipo='carrera', padre=fisei)
    sw_inf = NodoJerarquico.objects.create(nombre="Información General", tipo='area', padre=sw)
    Documento.objects.create(nombre="malla_curricular_2023.pdf", nodo=sw_inf)
    sw_s1 = NodoJerarquico.objects.create(nombre="Primer Semestre", tipo='area', padre=sw)
    Documento.objects.create(nombre="silabo_programacion_I.pdf", nodo=sw_s1)
    
    tics = NodoJerarquico.objects.create(nombre="Carrera de TICs", tipo='carrera', padre=fisei)
    rob = NodoJerarquico.objects.create(nombre="Carrera de Robótica e IA", tipo='carrera', padre=fisei)
    
    print("  - Estructura jerárquica inyectada.")

    # 6. Mapa de Espacios (Grafos)
    print("Mapeando espacios físicos y conexiones (Grafos)...")
    esp_map = {}
    
    # BLOQUE 1
    datos_b1 = [
        ("Entrada Principal", "B1-P1-ENT", "entrada", 1),
        ("Aula CTT", "B1-P1-CTT", "aula", 1),
        ("Dpto. Actividades Talleres", "B1-P1-DCTT", "oficina", 1),
        ("Aula 01", "B1-P1-A01", "aula", 1),
        ("Sala Profesores 1", "B1-P1-SP1", "oficina", 1),
        ("Escalera Bloque 1", "B1-P1-ESC", "pasillo", 1),
        ("Biblioteca FISEI", "B1-P2-BIB", "oficina", 2),
        ("Laboratorio 01", "B1-P2-L01", "laboratorio", 2),
        ("Decanato", "B1-P3-DEC", "oficina", 3),
    ]
    for n, c, t, p in datos_b1:
        esp_map[c] = EspacioFisico.objects.create(nombre=n, codigo=c, tipo=t, bloque="1", piso=p)

    # BLOQUE 2
    datos_b2 = [
        ("Entrada B2", "B2-P1-ENT", "entrada", 1),
        ("Aula S-01", "B2-PM1-A01", "aula", -1),
        ("Sala Profesores 2", "B2-P1-SP2", "oficina", 1),
        ("Aula 2-01", "B2-P2-A01", "aula", 2),
        ("Aula 3-01", "B2-P3-A01", "aula", 3),
        ("ASO Estudiantes", "B2-P4-ASO", "oficina", 4),
    ]
    for n, c, t, p in datos_b2:
        esp_map[c] = EspacioFisico.objects.create(nombre=n, codigo=c, tipo=t, bloque="2", piso=p)

    # CONEXIONES
    conexiones = [
        ("B1-P1-ENT", "B1-P1-CTT", 5.0),
        ("B1-P1-ENT", "B1-P1-DCTT", 6.0),
        ("B1-P1-ENT", "B1-P1-ESC", 8.0),
        ("B1-P1-ESC", "B1-P2-BIB", 10.0),
        ("B1-P2-BIB", "B1-P2-L01", 4.0),
        ("B1-P3-DEC", "B1-P1-ESC", 15.0),
        ("B1-P1-ENT", "B2-P1-ENT", 15.0),
        ("B2-P1-ENT", "B2-PM1-A01", 8.0),
        ("B2-P1-ENT", "B2-P1-SP2", 4.0),
        ("B2-P1-SP2", "B2-P2-A01", 10.0),
        ("B2-P2-A01", "B2-P3-A01", 6.0),
        ("B2-P3-A01", "B2-P4-ASO", 6.0),
    ]
    for o, d, p in conexiones:
        ConexionEspacio.objects.create(origen=esp_map[o], destino=esp_map[d], peso=p, bidireccional=True)
    print("  - Mapa completo inyectado.")

    # 7. Acciones Iniciales (Historial / Pila)
    print("Registrando historial inicial...")
    HistorialAccion.objects.create(usuario=user_objs['admin'], modulo='usuarios', accion='Configuración inicial')
    HistorialAccion.objects.create(usuario=user_objs['administrativo'], modulo='turnos', accion='Ventanillas habilitadas')

    print("\n=== CARGA DE DATOS FINALIZADA CON ÉXITO ===")
    print("Usuario Admin: admin@uta.edu.ec / Clave: Admin2026#")
    print("Usuario Estudiante: estudiante1@uta.edu.ec / Clave: Admin2026#")

if __name__ == "__main__":
    cargar_todo()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Tramite, TipoTramite, HistorialEstadoTramite
from .forms import TramiteSolicitudForm, TipoTramiteForm, CambioEstadoForm
from .services import ListaSecuencial, ListaDoble
from historial.utils import registrar_accion

# Estructuras de datos en memoria (Requisitos Académicos)
catalogo_tramites_memoria = ListaSecuencial(capacidad=50)
historial_estados_memoria = {} # tramite_id -> ListaDoble
tramites_usuario_memoria = {} # user_id -> ListaDoble

def inicializar_catalogo_completo():
    """Carga el catálogo institucional exacto solicitado."""
    datos_catalogo = [
        (1, "Certificado de matrícula", "Constancia oficial del período académico vigente", False),
        (2, "Récord académico", "Historial completo de calificaciones por asignatura", False),
        (3, "Certificado de egresamiento", "Constancia de haber aprobado todas las materias", False),
        (4, "Certificado de no adeudar", "Constancia de no tener deudas con la facultad", False),
        (5, "Permiso de ausencia", "Justificación oficial de inasistencias a clases", True),
        (6, "Solicitud de beca", "Postulación a programas de ayuda económica", True),
        (7, "Cambio de carrera", "Transferencia interna entre carreras de la FISEI", True),
        (8, "Homologación de materias", "Reconocimiento de asignaturas aprobadas en otra institución", True),
        (9, "Retiro de materia", "Solicitud formal de baja de una asignatura", True),
        (10, "Segunda matrícula", "Autorización para matricularse por segunda ocasión en una materia", True),
        (11, "Tercera matrícula", "Solicitud de matrícula extraordinaria con aval del consejo", True),
        (12, "Revisión de examen", "Impugnación formal de calificación obtenida", True),
        (13, "Constancia de horario", "Documento con el horario oficial del estudiante", False),
        (14, "Solicitud de práctica preprofesional", "Registro de inicio de horas prácticas externas", True),
        (15, "Titulación — tema de proyecto", "Aprobación del tema de trabajo de titulación", True),
    ]

    # 1. Asegurar persistencia en BD
    for id_p, nombre, desc, req in datos_catalogo:
        TipoTramite.objects.get_or_create(
            id=id_p,
            defaults={
                'nombre': nombre,
                'descripcion': desc,
                'requiere_documentos': req,
                'activo': True
            }
        )

    # 2. Sincronizar con Lista Secuencial en memoria (Req 1 y 5)
    if catalogo_tramites_memoria.tamaño() == 0:
        tipos_db = TipoTramite.objects.filter(activo=True).order_by('id')
        for t in tipos_db:
            catalogo_tramites_memoria.insertar(t)

@login_required
def solicitar_tramite_view(request):
    """Req 1: Estudiantes y docentes registran solicitudes usando Lista Secuencial."""
    if request.user.rol not in ['estudiante', 'docente', 'admin']:
        messages.error(request, "No tienes permisos para realizar trámites.")
        return redirect('usuarios:dashboard')

    inicializar_catalogo_completo()
    tipos_catalogo = catalogo_tramites_memoria.obtener_todos()

    if request.method == 'POST':
        form = TramiteSolicitudForm(request.POST)
        if form.is_valid():
            tramite = form.save(commit=False)
            tramite.solicitante = request.user
            count = Tramite.objects.count() + 1
            tramite.codigo = f"TR-{timezone.now().year}-{count:04d}"
            tramite.save()
            registrar_accion(request.user, 'tramites', 'Trámite registrado', f'Código {tramite.codigo}')
            
            # REQUISITO 3: Inicializar Historial con Lista Doble
            ld = ListaDoble()
            ld.agregar_al_final({
                'estado': 'pendiente',
                'fecha': timezone.now(),
                'responsable': 'Sistema'
            })
            historial_estados_memoria[tramite.id] = ld
            
            messages.success(request, f"Trámite {tramite.codigo} registrado con éxito.")
            return redirect('mis_tramites')
    else:
        form = TramiteSolicitudForm()
    
    # REQUISITO 1: Filtrar el queryset del formulario usando los IDs de la Lista Secuencial
    ids_catalogo = [t.id for t in tipos_catalogo if t is not None]
    form.fields['tipo'].queryset = TipoTramite.objects.filter(id__in=ids_catalogo)
    
    return render(request, 'tramites/solicitar.html', {
        'form': form,
        'tipos': tipos_catalogo,
        'sin_opciones': len(ids_catalogo) == 0
    })

@login_required
def detalle_tramite_usuario_view(request, tramite_id):
    """Req 4: Consulta detallada del usuario usando Lista Doble para el historial."""
    tramite = get_object_or_404(Tramite, id=tramite_id, solicitante=request.user)
    
    # Obtener historial para mostrar (usando la lista doble si existe en memoria)
    historial_lista = []
    if tramite.id in historial_estados_memoria:
        historial_lista = historial_estados_memoria[tramite.id].a_lista()
    else:
        # Reconstruir de la BD si no está en memoria
        ld = ListaDoble()
        for h in tramite.historial.all():
            ld.agregar_al_final({
                'estado': h.get_estado_nuevo_display(),
                'fecha': h.fecha,
                'responsable': h.responsable.username if h.responsable else 'Sistema',
                'observacion': h.observacion
            })
        historial_estados_memoria[tramite.id] = ld
        historial_lista = ld.a_lista()

    return render(request, 'tramites/detalle_usuario.html', {
        'tramite': tramite,
        'historial': historial_lista
    })

@login_required
def mis_tramites_view(request):
    """Req 4: Consulta de trámites propios usando Lista Doblemente Enlazada."""
    tramites_db = Tramite.objects.filter(solicitante=request.user).order_by('-fecha_registro')
    
    # REQUISITO 4: Cargar en Lista Doble
    ld = ListaDoble()
    for t in tramites_db:
        ld.agregar_al_final(t)
    
    tramites_usuario_memoria[request.user.id] = ld
    
    return render(request, 'tramites/mis_tramites.html', {
        'tramites': ld.a_lista()
    })

@login_required
def gestion_administrativa_view(request):
    """Req 2: Listado para que administrativos cambien estados."""
    if request.user.rol not in ['admin', 'administrativo']:
        return redirect('usuarios:dashboard')
    
    tramites = Tramite.objects.all().exclude(estado='archivado')
    return render(request, 'tramites/gestion_admin.html', {'tramites': tramites})

@login_required
def detalle_tramite_admin_view(request, tramite_id):
    """Req 3: Registro de cambios de estado usando Lista Doblemente Enlazada."""
    tramite = get_object_or_404(Tramite, id=tramite_id)
    
    if request.method == 'POST':
        form = CambioEstadoForm(request.POST)
        if form.is_valid():
            nuevo_h = form.save(commit=False)
            nuevo_h.tramite = tramite
            nuevo_h.estado_anterior = tramite.estado
            nuevo_h.responsable = request.user
            nuevo_h.save()
            
            tramite.estado = nuevo_h.estado_nuevo
            tramite.save()
            
            # REQUISITO 3: Actualizar Lista Doble en memoria
            if tramite.id not in historial_estados_memoria:
                historial_estados_memoria[tramite.id] = ListaDoble()
            
            historial_estados_memoria[tramite.id].agregar_al_final({
                'estado': nuevo_h.get_estado_nuevo_display(),
                'fecha': nuevo_h.fecha,
                'responsable': request.user.username,
                'observacion': nuevo_h.observacion
            })
            
            messages.success(request, "Estado actualizado correctamente.")
            return redirect('gestion_administrativa')
    else:
        form = CambioEstadoForm(initial={'estado_nuevo': tramite.estado})

    # Reconstruir historial de la BD si no está en memoria
    if tramite.id not in historial_estados_memoria:
        ld = ListaDoble()
        for h in tramite.historial.all():
            ld.agregar_al_final({
                'estado': h.get_estado_nuevo_display(),
                'fecha': h.fecha,
                'responsable': h.responsable.username if h.responsable else 'Sistema',
                'observacion': h.observacion
            })
        historial_estados_memoria[tramite.id] = ld

    return render(request, 'tramites/detalle_admin.html', {
        'tramite': tramite,
        'form': form,
        'historial': historial_estados_memoria[tramite.id].a_lista()
    })

@login_required
def gestionar_catalogo_view(request):
    """Req 5: Admin configura catálogo usando Lista Secuencial."""
    if request.user.rol != 'admin':
        return redirect('usuarios:dashboard')
    
    if request.method == 'POST':
        form = TipoTramiteForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            # REQUISITO 5: Insertar en lista secuencial
            catalogo_tramites_memoria.insertar(tipo)
            messages.success(request, "Catálogo actualizado.")
            return redirect('tramites:gestionar_catalogo')
    else:
        form = TipoTramiteForm()
    
    inicializar_catalogo_completo()
    return render(request, 'tramites/catalogo_admin.html', {
        'form': form,
        'tipos': catalogo_tramites_memoria.obtener_todos()
    })

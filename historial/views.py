from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from .models import HistorialAccion
from .services import PilaHistorial, ListaDoble
from tramites.models import Tramite, TipoTramite, HistorialEstadoTramite
from turnos.models import Turno
from usuarios.models import Usuario
from django.utils import timezone
from django.contrib import messages
from .utils import generar_pdf_reporte

@login_required
def HistorialAccionesView(request):
    # Carga las últimas 50 acciones del usuario
    acciones_db = HistorialAccion.objects.filter(usuario=request.user).order_by('fecha')[:50]
    
    # REQUISITO: Usar Pila para el historial
    pila = PilaHistorial(capacidad=50)
    for accion in acciones_db:
        pila.apilar(accion)
    
    acciones_lista = pila.a_lista()
    
    return render(request, 'historial/historial.html', {
        'acciones': acciones_lista,
        'total': len(acciones_lista)
    })

@login_required
def ReporteGeneralView(request):
    """Panel central de reportes para el administrador."""
    if request.user.rol != 'admin':
        raise PermissionDenied
    
    tipo_reporte = request.POST.get('tipo_reporte', 'tramites')
    tramites = None
    turnos = None
    usuarios = None
    resumen = None
    filtros = {'tipo_reporte': tipo_reporte}
    
    if request.method == 'POST':
        fecha_desde = request.POST.get('fecha_desde')
        fecha_hasta = request.POST.get('fecha_hasta')
        estado = request.POST.get('estado')
        
        if tipo_reporte == 'tramites':
            tipo_id = request.POST.get('tipo_id')
            tramites = Tramite.objects.all()
            if fecha_desde: tramites = tramites.filter(fecha_registro__date__gte=fecha_desde)
            if fecha_hasta: tramites = tramites.filter(fecha_registro__date__lte=fecha_hasta)
            if estado: tramites = tramites.filter(estado=estado)
            if tipo_id: tramites = tramites.filter(tipo_id=tipo_id)
            
            resumen = tramites.values('estado').annotate(total=Count('id'))
            resumen_dict = {item['estado']: item['total'] for item in resumen}
            resumen = {e: resumen_dict.get(e, 0) for e in ['pendiente', 'en_proceso', 'resuelto', 'archivado']}
            
        elif tipo_reporte == 'turnos':
            turnos = Turno.objects.all()
            if fecha_desde: turnos = turnos.filter(hora_solicitud__date__gte=fecha_desde)
            if fecha_hasta: turnos = turnos.filter(hora_solicitud__date__lte=fecha_hasta)
            if estado: turnos = turnos.filter(estado=estado)
            
            resumen = turnos.values('estado').annotate(total=Count('id'))
            resumen_dict = {item['estado']: item['total'] for item in resumen}
            resumen = {e: resumen_dict.get(e, 0) for e in ['espera', 'llamado', 'en_atencion', 'atendido', 'cancelado']}

        elif tipo_reporte in ['estudiantes', 'administradores']:
            rol_filtro = 'estudiante' if tipo_reporte == 'estudiantes' else 'admin'
            usuarios = Usuario.objects.filter(rol=rol_filtro)
            resumen = {'total': usuarios.count()}

        # Guardar filtros para repoblar form
        filtros.update({
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'estado': estado,
            'tipo_id': request.POST.get('tipo_id'),
        })

    tipos_tramite = TipoTramite.objects.all()
    
    return render(request, 'historial/reportes.html', {
        'tramites': tramites,
        'turnos': turnos,
        'usuarios': usuarios,
        'resumen': resumen,
        'tipos_tramite': tipos_tramite,
        'filtros': filtros
    })

@login_required
def exportar_pdf_view(request):
    """Vista para exportar los reportes actuales a PDF."""
    if request.user.rol != 'admin':
        raise PermissionDenied

    tipo_reporte = request.GET.get('tipo_reporte', 'tramites')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    estado = request.GET.get('estado')
    tipo_id = request.GET.get('tipo_id')

    if tipo_reporte == 'tramites':
        data_qs = Tramite.objects.all()
        if fecha_desde: data_qs = data_qs.filter(fecha_registro__date__gte=fecha_desde)
        if fecha_hasta: data_qs = data_qs.filter(fecha_registro__date__lte=fecha_hasta)
        if estado: data_qs = data_qs.filter(estado=estado)
        if tipo_id: data_qs = data_qs.filter(tipo_id=tipo_id)
        
        encabezados = ['Código', 'Solicitante', 'Tipo', 'Estado', 'Fecha']
        datos = [[t.codigo, t.solicitante.username, t.tipo.nombre, t.get_estado_display(), t.fecha_registro.strftime('%d/%m/%Y')] for t in data_qs]
        return generar_pdf_reporte("Reporte de Trámites", encabezados, datos, "reporte_tramites.pdf")

    elif tipo_reporte == 'turnos':
        data_qs = Turno.objects.all()
        if fecha_desde: data_qs = data_qs.filter(hora_solicitud__date__gte=fecha_desde)
        if fecha_hasta: data_qs = data_qs.filter(hora_solicitud__date__lte=fecha_hasta)
        if estado: data_qs = data_qs.filter(estado=estado)
        
        encabezados = ['Código', 'Usuario', 'Motivo', 'Estado', 'Fecha']
        datos = [[t.codigo, t.usuario.username, t.get_motivo_display(), t.get_estado_display(), t.hora_solicitud.strftime('%d/%m/%Y')] for t in data_qs]
        return generar_pdf_reporte("Reporte de Turnos", encabezados, datos, "reporte_turnos.pdf")

    elif tipo_reporte in ['estudiantes', 'administradores']:
        rol_filtro = 'estudiante' if tipo_reporte == 'estudiantes' else 'admin'
        data_qs = Usuario.objects.filter(rol=rol_filtro)
        
        encabezados = ['Usuario', 'Email', 'Nombre Completo', 'Cédula', 'Rol']
        datos = [[u.username, u.email, u.get_full_name(), u.cedula, u.get_rol_display()] for u in data_qs]
        titulo = "Reporte de Estudiantes" if tipo_reporte == 'estudiantes' else "Reporte de Administradores"
        return generar_pdf_reporte(titulo, encabezados, datos, f"reporte_{tipo_reporte}.pdf")

    return redirect('historial:reportes')

@login_required
def ExpedientesActivosView(request):
    if request.user.rol not in ['estudiante', 'docente']:
        messages.error(request, "Solo estudiantes y docentes pueden acceder a sus expedientes.")
        return redirect('usuarios:dashboard')
        
    tramites_activos = Tramite.objects.filter(solicitante=request.user).exclude(estado='archivado').order_by('fecha_registro')
    total = tramites_activos.count()
    
    if total == 0:
        return render(request, 'historial/expedientes.html', {'total_expedientes': 0})
        
    # REQUISITO: Usar Lista Doblemente Enlazada
    lista_doble = ListaDoble()
    for t in tramites_activos:
        lista_doble.agregar_al_final(t)
        
    # Navegación
    posicion = int(request.GET.get('posicion', 0))
    accion = request.GET.get('accion')
    
    if accion == 'siguiente' and posicion < total - 1:
        posicion += 1
    elif accion == 'anterior' and posicion > 0:
        posicion -= 1
        
    expediente_actual = lista_doble.obtener_en_posicion(posicion)
    
    historial_estados = HistorialEstadoTramite.objects.filter(tramite=expediente_actual).order_by('fecha')
    
    return render(request, 'historial/expedientes.html', {
        'expediente_actual': expediente_actual,
        'historial_estados': historial_estados,
        'posicion_actual': posicion,
        'total_expedientes': total,
        'tiene_anterior': posicion > 0,
        'tiene_siguiente': posicion < total - 1
    })

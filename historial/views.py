from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from .models import HistorialAccion
from .services import PilaHistorial, ListaDoble
from tramites.models import Tramite, TipoTramite, HistorialEstadoTramite
from django.utils import timezone

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
def ReporteTramitesView(request):
    if request.user.rol != 'admin':
        raise PermissionDenied
    
    tramites = None
    resumen = None
    filtros = {}
    
    if request.method == 'POST':
        fecha_desde = request.POST.get('fecha_desde')
        fecha_hasta = request.POST.get('fecha_hasta')
        estado = request.POST.get('estado')
        tipo_id = request.POST.get('tipo_id')
        
        tramites = Tramite.objects.all()
        
        if fecha_desde:
            tramites = tramites.filter(fecha_registro__date__gte=fecha_desde)
            filtros['fecha_desde'] = fecha_desde
        if fecha_hasta:
            tramites = tramites.filter(fecha_registro__date__lte=fecha_hasta)
            filtros['fecha_hasta'] = fecha_hasta
        if estado:
            tramites = tramites.filter(estado=estado)
            filtros['estado'] = estado
        if tipo_id:
            tramites = tramites.filter(tipo_id=tipo_id)
            filtros['tipo_id'] = int(tipo_id)
            
        # Calcular resumen
        resumen = tramites.values('estado').annotate(total=Count('id'))
        resumen_dict = {item['estado']: item['total'] for item in resumen}
        # Asegurar que todos los estados estén en el dict aunque sea con 0
        estados_posibles = ['pendiente', 'en_proceso', 'resuelto', 'archivado']
        resumen = {e: resumen_dict.get(e, 0) for e in estados_posibles}

    tipos = TipoTramite.objects.all()
    
    return render(request, 'historial/reportes.html', {
        'tramites': tramites,
        'resumen': resumen,
        'tipos': tipos,
        'filtros': filtros
    })

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

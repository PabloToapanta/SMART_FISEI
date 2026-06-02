from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Turno, Ventanilla
from .forms import TurnoSolicitudForm
from .services import ColaFIFO, ListaCircular
from historial.services import PilaHistorial
from historial.models import HistorialAccion
from historial.utils import registrar_accion
import random

# Instancias globales en memoria para el proyecto de Estructura de Datos
cola_espera = ColaFIFO()
ventanillas_rotativas = ListaCircular()
pila_historial = PilaHistorial(capacidad=20)

def inicializar_estructuras():
    """Carga las ventanillas en la lista circular y sincroniza la cola si es necesario."""
    # Inicializar ventanillas si la lista circular está vacía
    if ventanillas_rotativas.tamaño() == 0:
        ventanillas = Ventanilla.objects.filter(activa=True)
        for v in ventanillas:
            ventanillas_rotativas.agregar(v)
    
    # Sincronizar cola con la DB si la memoria está vacía pero hay turnos en espera
    if cola_espera.esta_vacia():
        turnos_pendientes = Turno.objects.filter(estado='espera').order_by('hora_solicitud')
        for t in turnos_pendientes:
            cola_espera.encolar(t.id)

@login_required
def solicitar_turno_view(request):
    if request.user.rol not in ['estudiante', 'docente', 'admin']:
        messages.error(request, "Solo estudiantes y docentes pueden solicitar turnos.")
        return redirect('usuarios:dashboard')
        
    inicializar_estructuras()
    if request.method == 'POST':
        form = TurnoSolicitudForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.usuario = request.user
            
            # Generar código simple T-00X
            count = Turno.objects.count() + 1
            turno.codigo = f"T-{count:03d}"
            
            # REQUISITO: Lista Circular para distribuir ventanillas
            ventanilla_asignada = ventanillas_rotativas.siguiente_ventanilla()
            if ventanilla_asignada:
                turno.ventanilla = ventanilla_asignada
            
            turno.save()
            
            # REQUISITO: Cola FIFO para encolar el turno
            cola_espera.encolar(turno.id)
            registrar_accion(request.user, 'turnos', 'Turno solicitado', f'Código {turno.codigo}')
            
            messages.success(request, f"Turno {turno.codigo} solicitado con éxito. Por favor espere.")
            return redirect('turnos:estado_cola')
    else:
        form = TurnoSolicitudForm()
    
    return render(request, 'turnos/solicitar.html', {'form': form})

@login_required
def dashboard_administrativo_view(request):
    """Panel para que el personal administrativo llame turnos."""
    if request.user.rol not in ['admin', 'administrativo']:
        return redirect('usuarios:dashboard')
    
    inicializar_estructuras()
    
    # Obtener el turno que está siendo llamado o atendido en ESTA ventanilla
    ventanilla = Ventanilla.objects.filter(responsable=request.user).first()
    
    turno_actual_llamado = Turno.objects.filter(ventanilla=ventanilla, estado='llamado').first()
    turno_actual_atencion = Turno.objects.filter(ventanilla=ventanilla, estado='en_atencion').first()
    
    return render(request, 'turnos/atencion.html', {
        'turno_actual_llamado': turno_actual_llamado,
        'turno_actual_atencion': turno_actual_atencion,
        'cola_vacia': cola_espera.esta_vacia(),
        'historial_pila': pila_historial.a_lista()
    })

@login_required
def llamar_siguiente_view(request):
    if request.user.rol not in ['admin', 'administrativo']:
        return redirect('usuarios:dashboard')
    
    inicializar_estructuras()
    
    # REQUISITO: Desencolar (FIFO)
    turno_id = cola_espera.desencolar()
    
    if turno_id:
        turno = get_object_or_404(Turno, id=turno_id)
        # Cambio de flujo: primero se llama
        turno.estado = 'llamado'
        # Asignar a la ventanilla del administrativo que llama
        ventanilla = Ventanilla.objects.filter(responsable=request.user).first()
        if ventanilla:
            turno.ventanilla = ventanilla
        turno.save()
        messages.success(request, f"Llamando al turno {turno.codigo}")
    else:
        messages.warning(request, "No hay turnos en espera.")
        
    return redirect('turnos:dashboard_administrativo')

@login_required
def iniciar_atencion_view(request, turno_id):
    """Paso para pasar de 'llamado' a 'en_atencion'."""
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'en_atencion'
    turno.hora_inicio_atencion = timezone.now()
    turno.save()
    messages.info(request, f"Atendiendo a {turno.usuario.username}")
    return redirect('turnos:dashboard_administrativo')

@login_required
def finalizar_atencion_view(request, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    turno.estado = 'atendido'
    turno.hora_fin_atencion = timezone.now()
    turno.save()
    
    # REQUISITO: Pila para el historial reciente
    accion = f"Atención finalizada: {turno.codigo}"
    pila_historial.apilar({
        'usuario': request.user.username,
        'accion': accion,
        'fecha': timezone.now().strftime("%H:%M:%S")
    })
    
    # Persistir en la base de datos también
    HistorialAccion.objects.create(
        usuario=request.user,
        modulo='turnos',
        accion=accion,
        detalle=f"Motivo: {turno.get_motivo_display()}. Solicitado por: {turno.usuario.username}"
    )
    
    messages.success(request, "Atención finalizada y registrada en el historial.")
    return redirect('turnos:dashboard_administrativo')

@login_required
def estado_cola_view(request):
    """Vista pública del estado de la cola."""
    inicializar_estructuras()
    espera = Turno.objects.filter(estado='espera').order_by('hora_solicitud')
    atencion = Turno.objects.filter(estado='en_atencion')
    atendidos = Turno.objects.filter(estado='atendido').order_by('-hora_fin_atencion')[:5]
    
    return render(request, 'turnos/estado_cola.html', {
        'espera': espera,
        'atencion': atencion,
        'atendidos': atendidos,
        'en_cola_memoria': cola_espera.tamaño()
    })

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import EspacioFisico, ConexionEspacio
from .services import Grafo

def obtener_datos_grafo():
    espacios = EspacioFisico.objects.filter(activo=True)
    conexiones = ConexionEspacio.objects.all()
    
    espacios_data = []
    for e in espacios:
        espacios_data.append({
            'id': e.id,
            'label': f"{e.codigo}\n{e.nombre[:15]}...",
            'title': e.nombre,
            'tipo': e.tipo,
            'bloque': e.bloque,
            'piso': e.piso
        })
        
    conexiones_data = []
    for c in conexiones:
        conexiones_data.append({
            'from': c.origen_id,
            'to': c.destino_id,
            'label': f"{c.peso}m",
            'weight': c.peso,
            'bidirectional': c.bidireccional
        })
        
    return json.dumps(espacios_data), json.dumps(conexiones_data)

@login_required
def mapa_view(request):
    espacios_json, conexiones_json = obtener_datos_grafo()
    espacios_select = EspacioFisico.objects.filter(activo=True).exclude(tipo='pasillo').order_by('bloque', 'piso', 'nombre')
    
    return render(request, 'rutas/mapa.html', {
        'espacios_json': espacios_json,
        'conexiones_json': conexiones_json,
        'espacios_select': espacios_select
    })

@login_required
def buscar_ruta_view(request):
    espacios_json, conexiones_json = obtener_datos_grafo()
    espacios_select = EspacioFisico.objects.filter(activo=True).exclude(tipo='pasillo').order_by('bloque', 'piso', 'nombre')
    
    ruta_ids = []
    distancia_total = 0
    espacios_ruta = []
    busqueda_realizada = False

    if request.method == 'POST':
        busqueda_realizada = True
        origen_id = int(request.POST.get('origen_id'))
        destino_id = int(request.POST.get('destino_id'))
        
        conexiones = ConexionEspacio.objects.all()
        grafo = Grafo()
        grafo.construir_desde_db(conexiones)
        
        ruta_ids, distancia_total = grafo.dijkstra(origen_id, destino_id)
        
        if ruta_ids:
            espacios_ruta = [EspacioFisico.objects.get(id=rid) for rid in ruta_ids]

    return render(request, 'rutas/mapa.html', {
        'espacios_json': espacios_json,
        'conexiones_json': conexiones_json,
        'espacios_select': espacios_select,
        'ruta_ids': ruta_ids,
        'distancia_total': distancia_total,
        'espacios_ruta': espacios_ruta,
        'busqueda_realizada': busqueda_realizada
    })

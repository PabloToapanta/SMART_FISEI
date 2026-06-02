from .models import HistorialAccion

def registrar_accion(usuario, modulo, accion, detalle=''):
    """Registra una acción importante en la base de datos."""
    HistorialAccion.objects.create(
        usuario=usuario, 
        modulo=modulo, 
        accion=accion, 
        detalle=detalle
    )

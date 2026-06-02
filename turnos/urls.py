from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
    path('solicitar/', views.solicitar_turno_view, name='solicitar_turno'),
    path('atencion/', views.dashboard_administrativo_view, name='dashboard_administrativo'),
    path('llamar/', views.llamar_siguiente_view, name='llamar_siguiente'),
    path('iniciar/<int:turno_id>/', views.iniciar_atencion_view, name='iniciar_atencion'),
    path('finalizar/<int:turno_id>/', views.finalizar_atencion_view, name='finalizar_atencion'),
    path('estado/', views.estado_cola_view, name='estado_cola'),
]

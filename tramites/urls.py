from django.urls import path
from . import views

app_name = 'tramites'

urlpatterns = [
    path('solicitar/', views.solicitar_tramite_view, name='solicitar_tramite'),
    path('mis-tramites/', views.mis_tramites_view, name='mis_tramites'),
    path('mi-detalle/<int:tramite_id>/', views.detalle_tramite_usuario_view, name='detalle_tramite_usuario'),
    path('catalogo/', views.gestionar_catalogo_view, name='gestionar_catalogo'),
    path('gestion/', views.gestion_administrativa_view, name='gestion_administrativa'),
    path('detalle/<int:tramite_id>/', views.detalle_tramite_admin_view, name='detalle_tramite_admin'),
]

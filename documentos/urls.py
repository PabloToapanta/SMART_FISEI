from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    path('jerarquia/', views.jerarquia_view, name='jerarquia'),
    path('nodo/nuevo/', views.gestionar_nodo_view, name='crear_nodo'),
    path('nodo/editar/<int:nodo_id>/', views.gestionar_nodo_view, name='editar_nodo'),
    path('nodo/eliminar/<int:nodo_id>/', views.eliminar_nodo_view, name='eliminar_nodo'),
    path('documento/subir/', views.subir_documento_view, name='subir_documento'),
    path('documento/ver/<int:doc_id>/', views.consultar_documento_view, name='ver_documento'),
]

from django.urls import path
from . import views

app_name = 'rutas'

urlpatterns = [
    path('', views.mapa_view, name='mapa'),
    path('buscar/', views.buscar_ruta_view, name='buscar_ruta'),
]

from django.urls import path
from . import views

app_name = 'historial'

urlpatterns = [
    path('', views.HistorialAccionesView, name='historial'),
    path('reportes/', views.ReporteGeneralView, name='reportes'),
    path('reportes/exportar/', views.exportar_pdf_view, name='exportar_pdf'),
    path('expedientes/', views.ExpedientesActivosView, name='expedientes'),
]

from django.urls import path
from . import views

app_name = 'historial'

urlpatterns = [
    path('', views.HistorialAccionesView, name='historial'),
    path('reportes/', views.ReporteTramitesView, name='reportes'),
    path('expedientes/', views.ExpedientesActivosView, name='expedientes'),
]

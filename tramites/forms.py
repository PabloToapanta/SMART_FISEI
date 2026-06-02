from django import forms
from .models import Tramite, TipoTramite, HistorialEstadoTramite

class TipoTramiteForm(forms.ModelForm):
    class Meta:
        model = TipoTramite
        fields = ['nombre', 'descripcion', 'activo', 'requiere_documentos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requiere_documentos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TramiteSolicitudForm(forms.ModelForm):
    class Meta:
        model = Tramite
        fields = ['tipo', 'descripcion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CambioEstadoForm(forms.ModelForm):
    class Meta:
        model = HistorialEstadoTramite
        fields = ['estado_nuevo', 'observacion']
        widgets = {
            'estado_nuevo': forms.Select(choices=Tramite.ESTADO_CHOICES, attrs={'class': 'form-select'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

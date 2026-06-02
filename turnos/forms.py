from django import forms
from .models import Turno

class TurnoSolicitudForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['motivo']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-select'}),
        }

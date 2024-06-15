from django import forms
#aqui los modelos para usar los formularios
from .models import *
from django import forms
from .models import Agenda, Cita

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['fecha_disponible', 'hora_disponible', 'especialista', 'centro_medico']

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mensaje']
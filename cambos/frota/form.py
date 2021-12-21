from django import forms
from .models import Viagem
from django_select2.forms import Select2Widget


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = (
            'veiculo',
            'motorista',
            'data',
            'origem',
            'destino',
            'carga',
            'peso',
            'km_inicial',
            'km_final'
        )
         
        widgets = {                                     
            'veiculo': Select2Widget(                
                attrs={'class':'form-control', 'autofocus': 'autofocus'},                
            ),
            'peso': forms.NumberInput(attrs={'class':'form-control'}),
        }
    

from django import forms
from .models import Viagem
from django_select2.forms import Select2Widget


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = (
            'data',
            'veiculo',
            'motorista',            
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
            'motorista': Select2Widget(                
                attrs={'class':'form-control', 'autofocus': 'autofocus'},                
            ),
            'data': forms.DateInput(attrs={'class':'form-control'}),
            'peso': forms.NumberInput(attrs={'class':'form-control'}),
            'origem': forms.TextInput(attrs={'class':'form-control'}),
            'destino': forms.TextInput(attrs={'class':'form-control'}),
            'carga': forms.TextInput(attrs={'class':'form-control'}),
            'km_inicial': forms.NumberInput(attrs={'class':'form-control'}),
            'km_final': forms.NumberInput(attrs={'class':'form-control'}),
        }
    

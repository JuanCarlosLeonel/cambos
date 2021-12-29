from django import forms
from .models import Viagem, Abastecimento
from django_select2.forms import Select2Widget


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = (            
            'veiculo',
            'motorista',            
            'data_inicial',
            'data_final',
            'hora_inicial',
            'hora_final',            
            'destino',            
            'km_inicial',
            'km_final'
        )
         
        widgets = {                                     
            'veiculo': forms.HiddenInput(),
            'motorista': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'data_inicial':forms.DateInput(attrs={'class':'form-control datepicker'}),            
            'data_final':forms.DateInput(attrs={'class':'form-control datepicker'}),     
            'hora_inicial': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'hora_final': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'destino': forms.TextInput(attrs={'class':'form-control'}),            
            'km_inicial': forms.NumberInput(attrs={'class':'form-control'}),
            'km_final': forms.NumberInput(attrs={'class':'form-control'}),
        }


class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = (            
            'veiculo',
            'data',
            'valor_unitario',            
            'quantidade',            
        )
         
        widgets = {                                     
            'veiculo': Select2Widget(                
                attrs={'class':'form-control', 'autofocus': 'autofocus'},                
            ),            
            'data': forms.DateInput(attrs={'class':'form-control'}),
            'valor_unitario': forms.NumberInput(attrs={'class':'form-control'}),            
            'quantidade': forms.NumberInput(attrs={'class':'form-control'}),
        }


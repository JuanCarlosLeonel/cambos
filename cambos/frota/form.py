from django import forms
from .models import Viagem, Abastecimento
from django_select2.forms import Select2Widget


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = (            
            'veiculo',
            'motorista',            
            'destino',                        
            'data_inicial',
            'hora_inicial',
            'km_inicial',
            'data_final',            
            'hora_final',                        
            'km_final'
        )
         
        widgets = {                                     
            'veiculo': forms.HiddenInput(),
            'motorista': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'data_inicial':forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),            
            'data_final':forms.DateInput(attrs={'class':'form-control datepicker'}),     
            'hora_inicial': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'hora_final': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'destino': forms.TextInput(attrs={'class':'form-control'}),            
            'km_inicial': forms.NumberInput(attrs={'class':'form-control'}),
            'km_final': forms.NumberInput(attrs={'class':'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ViagemForm, self).__init__(*args, **kwargs)
        self.fields['data_inicial'].label = "Data Saída"
        self.fields['hora_inicial'].label = "Hora Saída"
        self.fields['data_final'].label = "Data Retorno"
        self.fields['hora_final'].label = "Hora Retorno"

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


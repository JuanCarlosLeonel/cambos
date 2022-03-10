from random import choices
from django import forms


from .models import Manutencao, Viagem, Abastecimento
from django_select2.forms import Select2Widget

from frota import models


class ViagemForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = (            
            'veiculo',
            'tipo',
            'motorista',
            'motorista2',
            'ajudante',
            'origem',            
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
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'motorista': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'motorista2': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'ajudante': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'data_inicial':forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),            
            'data_final':forms.DateInput(attrs={'class':'form-control datepicker'}),     
            'hora_inicial': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'hora_final': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),   
            'origem': forms.TextInput(attrs={'class':'form-control'}),         
            'destino': forms.TextInput(attrs={'class':'form-control'}),            
            'km_inicial': forms.NumberInput(attrs={'class':'form-control'}),
            'km_final': forms.NumberInput(attrs={'class':'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        list_motorista = kwargs.pop('list_motorista', None)
        super(ViagemForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].label = "Saída para"
        self.fields['data_inicial'].label = "Data Saída"
        self.fields['hora_inicial'].label = "Hora Saída"
        self.fields['data_final'].label = "Data Retorno"
        self.fields['hora_final'].label = "Hora Retorno"
        if list_motorista:
            self.fields['motorista'].queryset = models.Pessoa.objects.filter(id__in = list_motorista)
            self.fields['motorista2'].queryset = models.Pessoa.objects.filter(id__in = list_motorista)
            self.fields['ajudante'].queryset = models.Pessoa.objects.filter(status = 0) #PEGAR APENAS COLABORADORES ATIVOS DA TABELA SOUZACAMBOS.COLABORADORS
        else:
            self.fields['motorista'].queryset = models.Pessoa.objects.filter(status = 0) #PEGAR APENAS COLABORADORES ATIVOS DA TABELA SOUZACAMBOS.COLABORADORS
            self.fields['motorista2'].widget = forms.HiddenInput()
            self.fields['ajudante'].widget = forms.HiddenInput()

class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = (         
            'veiculo',
            'interno',
            'combustivel',
            'data',
            'valor_unitario',            
            'quantidade',            
        )
         
        widgets = {                                    
            'veiculo': forms.HiddenInput(),        
            'combustivel': forms.Select(attrs={'class':'form-control'}),
            'data': forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),
            'valor_unitario': forms.NumberInput(attrs={'class':'form-control'}),            
            'quantidade': forms.NumberInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        inter = kwargs.pop('inter', None)                
        super().__init__(*args, **kwargs)
        self.fields['valor_unitario'].label = "Valor Total"
        self.fields['interno'].label = "INTERNO"
        if not inter:
            self.fields['interno'].widget = forms.HiddenInput()

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = (            
            'veiculo',
            'km',
            'manutencao',
            'valor',            
            'descricao', 
            'data_criacao',           
        )
         
        widgets = {                                     
            'veiculo': Select2Widget(                
                attrs={'class':'form-control', 'autofocus': 'autofocus'},                
            ),       
            'km': forms.TextInput(attrs={'class':'form-control'}),  
            'manutencao': forms.Select(attrs={'class':'form-control'}),
            'data_criacao': forms.DateInput(attrs={'class':'form-control datepicker'}),
            'valor': forms.NumberInput(attrs={'class':'form-control'}),            
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
        }


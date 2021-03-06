from random import choices
from django import forms

from core.models import Enderecos
from .models import ControleVisitantes, Manutencao, Viagem, Abastecimento, SolicitacaoViagem, Servicos
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
        self.fields['tipo'].label = "Sa??da para"
        self.fields['data_inicial'].label = "Data Sa??da"
        self.fields['hora_inicial'].label = "Hora Sa??da"
        self.fields['data_final'].label = "Data Retorno"
        self.fields['hora_final'].label = "Hora Retorno"
        if list_motorista:
            self.fields['hora_inicial'].widget = forms.HiddenInput()
            self.fields['motorista'].queryset = models.Pessoa.objects.filter(id__in = list_motorista)
            self.fields['motorista2'].queryset = models.Pessoa.objects.filter(id__in = list_motorista)
            self.fields['ajudante'].queryset = models.Pessoa.objects.filter(status = 0) #PEGAR APENAS COLABORADORES ATIVOS DA TABELA SOUZACAMBOS.COLABORADORS
        else:
            self.fields['motorista'].queryset = models.Pessoa.objects.filter(status = 0) #PEGAR APENAS COLABORADORES ATIVOS DA TABELA SOUZACAMBOS.COLABORADORS
            self.fields['motorista2'].widget = forms.HiddenInput()
            self.fields['ajudante'].widget = forms.HiddenInput()


class ViagemPortariaForm(forms.ModelForm):
    class Meta:
        model = Viagem
        fields = (
            'motorista',
            'motorista2',
            'data_inicial',
            'km_inicial',
            'hora_inicial',
            'data_final',
            'hora_final',
            'km_final'
        )

        widgets = {
            'motorista': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'motorista2': Select2Widget(                
                attrs={'class':'form-control'},                
            ),
            'data_inicial':forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),            
            'data_final':forms.DateInput(attrs={'class':'form-control datepicker'}),     
            'hora_inicial': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'hora_final': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),
            'km_inicial': forms.NumberInput(attrs={'class':'form-control'}),
            'km_final': forms.NumberInput(attrs={'class':'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        list_motorista = kwargs.pop('list_motorista', None)
        super(ViagemPortariaForm, self).__init__(*args, **kwargs)
        self.fields['data_inicial'].label = "Data Sa??da"
        self.fields['hora_inicial'].label = "Hora Sa??da"
        self.fields['data_final'].label = "Data Retorno"
        self.fields['hora_final'].label = "Hora Retorno"
        if list_motorista:
            self.fields['motorista'].queryset = models.Pessoa.objects.filter(id__in = list_motorista)
            self.fields['motorista2'].queryset = models.Pessoa.objects.filter(id__in = list_motorista)
        else:
            self.fields['motorista'].queryset = models.Pessoa.objects.filter(status = 0) #PEGAR APENAS COLABORADORES ATIVOS DA TABELA SOUZACAMBOS.COLABORADORS
            self.fields['motorista2'].widget = forms.HiddenInput()

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
            'responsavel',         
        )
         
        widgets = {                                    
            'veiculo': forms.HiddenInput(),        
            'combustivel': forms.Select(attrs={'class':'form-control'}),
            'data': forms.HiddenInput(),
            'valor_unitario': forms.NumberInput(attrs={'class':'form-control'}),            
            'quantidade': forms.NumberInput(attrs={'class':'form-control'}),
            'responsavel': forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        inter = kwargs.pop('inter', None)   
        valor = kwargs.pop('valor', None)              
        super().__init__(*args, **kwargs)
        self.fields['valor_unitario'].label = "Valor Total"
        self.fields['interno'].label = "INTERNO"
        self.fields['responsavel'].label = "RESPONS??VEL"
        if not inter:
            self.fields['interno'].widget = forms.HiddenInput()
        if inter:
            self.fields['combustivel'].widget = forms.HiddenInput()
        if valor:
            self.fields['valor_unitario'].widget = forms.HiddenInput()
            self.fields['combustivel'].widget = forms.HiddenInput()
            self.fields['interno'].widget = forms.HiddenInput()


class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoViagem
        fields = (         
            'endereco',
            'user',
            'data_prevista',
            'tipo',             
            'prioridade',
            'peso',
            'quantidade',
            'produtos',
            'horaentrega_coleta',
            'data_solicitacao',     
        )
         
        widgets = {             
            'endereco': Select2Widget(                
                attrs={'class':'form-control'},                
            ),                       
            'user': Select2Widget(                
                attrs={'class':'form-control'},                
            ),      
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'prioridade': forms.Select(attrs={'class':'form-control'}),
            'peso': forms.NumberInput(attrs={'class':'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class':'form-control'}),
            'horaentrega_coleta': forms.TextInput(attrs={'class':'form-control'}),
            'produtos': forms.TextInput(attrs={'class':'form-control'}),
            'data_prevista': forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),
            'data_solicitacao': forms.HiddenInput(),  
        }

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)       
        self.fields['user'].label = "Solicitante"
        self.fields['produtos'].label = "Produto"
        self.fields['horaentrega_coleta'].label = "Hor??rio de Entrega/Coleta"


class SolicitacaoMotoristaForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoViagem
        fields = (         
            'data_finalizacao',      
        )
         
        widgets = {             
            'data_finalizacao': forms.DateTimeInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),    
        }


class VisitanteForm(forms.ModelForm):
    class Meta:
        model  = ControleVisitantes
        fields = (
            'data',
            'nome',
            'documento',
            'hora_inicial',
            'hora_final',
            'responsavel',
        )

        widgets = {
            'data': forms.HiddenInput(),
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'documento': forms.TextInput(attrs={'class':'form-control'}),
            'hora_inicial': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),            
            'hora_final': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),
            'responsavel': forms.TextInput(attrs={'class':'form-control'}),
        }


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Enderecos
        fields = (
            'endereco',
            'bairro',
            'numero',
            'cidade',
            'uf',
            'cep',
        )

        widgets = {             
            'endereco': forms.TextInput(attrs={'class':'form-control'}),                       
            'bairro': forms.TextInput(attrs={'class':'form-control'}),    
            'numero': forms.NumberInput(attrs={'class':'form-control'}), 
            'cidade': forms.TextInput(attrs={'class':'form-control'}),
            'uf': forms.TextInput(attrs={'class':'form-control'}),
            'cep': forms.NumberInput(attrs={'class':'form-control'}),     
        }
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)       
        self.fields['endereco'].label = "Rua"


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


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servicos
        fields = (            
            'motorista',
            'empilhadeira',            
            'data_inicial',
            'hora_inicial', 
            'tipo_servico',
            'descricao', 
            'tipo_manutencao',
            # 'data_final',            
            # 'hora_final',    
        )
         
        widgets = {     
            'motorista': Select2Widget(                
                attrs={'class':'form-control'},                
            ),                                
            'empilhadeira': Select2Widget(                
                attrs={'class':'form-control', 'autofocus': 'autofocus'},                
            ),  
            'descricao': forms.TextInput(attrs={'class':'form-control'}),     
            'data_inicial':forms.HiddenInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}), 
            'hora_inicial': forms.HiddenInput(attrs={'data-mask':'00:00','class':'form-control'}),   
            'tipo_servico': forms.Select(attrs={'class':'form-control'}),
            'tipo_manutencao': forms.Select(attrs={'class':'form-control'}),
            # 'data_final':forms.DateInput(attrs={'class':'form-control datepicker'}),                
            # 'hora_final': forms.TimeInput(attrs={'data-mask':'00:00','class':'form-control'}),          
        }
        
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)       
        self.fields['motorista'].queryset = models.Motorista.objects.filter(empilhadeirista=True)
        self.fields['empilhadeira'].queryset = models.Veiculo.objects.filter(empilhadeira=True)
        self.fields['motorista'].label = "Colaborador"
        self.fields['descricao'].label = "Servi??o Prestado"

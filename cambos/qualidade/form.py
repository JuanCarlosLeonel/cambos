from django.forms import ModelForm, fields, widgets
from django import forms
from .models import Acao, PlanoDeAcao
from django_select2.forms import Select2Widget
from core.models import User


class PlanoAcaoForm(forms.ModelForm):
        class Meta:
            model = PlanoDeAcao
            fields = ['tipo_acao', 'origem_acao', 'tipo_referencia', 'referencia']
        
            widgets = {                         
                'tipo_acao': forms.Select(attrs={'class':'form-control'}),
                'origem_acao': forms.Select(attrs={'class':'form-control'}),
                'tipo_referencia': forms.Select(attrs={'class':'form-control'}),
                'referencia': forms.TextInput(attrs={'class':'form-control'})            
                }


class AcaoForm(forms.ModelForm):
    class Meta:
        model = Acao
        fields= ['plano_acao','descricao','responsavel', 'data_prazo', 'data_inicio', 'data_fim', 'resposta']

        widgets = {                         
                'plano_acao': forms.TextInput(attrs={'class':'form-control'}),            
                'descricao': forms.TextInput(attrs={'class':'form-control'}),            
                'responsavel': Select2Widget(attrs={'class':'form-control'}), 
                'data_prazo': forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),                
                'data_inicio': forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),                
                'data_fim': forms.DateInput(attrs={'data-mask':'00/00/0000','class':'form-control datepicker'}),                
                'resposta': forms.TextInput(attrs={'class':'form-control'}),            
                }

    def __init__(self, *args, **kwargs):
        usuario_list = kwargs.pop('usuario_list', None)
        super(AcaoForm, self).__init__(*args, **kwargs)                
        self.fields['responsavel'].queryset = User.objects.filter(id__in = usuario_list)
    
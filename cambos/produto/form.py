from django import forms
from .models import Producao, Material, Desempenho
from django_select2.forms import Select2Widget


class ProducaoModalForm(forms.ModelForm):
    class Meta:
        model = Producao
        fields = (
            'periodo',
            'setor',
            'material',
            'quantidade'
        )

        widgets = {                         
            'periodo': forms.HiddenInput(),
            'setor': forms.HiddenInput(),
            'material': forms.HiddenInput(),
            'quantidade': forms.NumberInput(attrs={'class':'form-control', 'autofocus': 'autofocus'}),
        } 


class ProducaoForm(forms.ModelForm):
    class Meta:
        model = Producao
        fields = (
            'periodo',
            'setor',
            'material',
            'quantidade'
        )
         
        widgets = {                         
            'periodo': forms.HiddenInput(),
            'setor': forms.HiddenInput(),
            'material': Select2Widget(                
                attrs={'class':'form-control', 'autofocus': 'autofocus'},                
            ),
            'quantidade': forms.NumberInput(attrs={'class':'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):        
        produzidos = kwargs.pop('produzidos', None)
        super().__init__(*args, **kwargs)

        self.fields['material'].queryset = self.fields['material'].queryset.filter(            
            tipo="Material"            
        ).order_by(
            'nome'
        ).exclude(
            id__in = produzidos
        )

class MaterialProducaoForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = (
            'cod',
            'nome',
            'origem',
            'tipo',
            'unidade',            
        )
        widgets = {                         
            'cod': forms.NumberInput(attrs={'class':'form-control'}),
            'nome': forms.TextInput(attrs={'class':'form-control'}),
            'origem': forms.HiddenInput(),
            'tipo': forms.HiddenInput(),
            'unidade': forms.HiddenInput(),            
        }


class DesempenhoForm(forms.ModelForm):
    class Meta:
        model = Desempenho
        fields = (
            'setor',
            'periodo',            
            'capacidade_total',
            'dias_trabalhados',
            'total_planejado',
            'headcount',
            'expedidores',
            'revisores',
            'setup',
            'carga_descarga',
            'manutencao_corretiva',
            'manutencao_preventiva',
            'total_alvejado',
            'total_chamuscado',
            'total_expedido',
            'total_recebido',
            'total_tingido',            
        )
        widgets = {                         
            'periodo': forms.HiddenInput(),
            'setor': forms.HiddenInput(),
            'capacidade_total':forms.NumberInput(attrs={'class':'form-control'}),
            'dias_trabalhados':forms.NumberInput(attrs={'class':'form-control'}),
            'total_planejado':forms.NumberInput(attrs={'class':'form-control'}),
            'headcount':forms.NumberInput(attrs={'class':'form-control'}),
            'expedidores':forms.NumberInput(attrs={'class':'form-control'}),
            'revisores':forms.NumberInput(attrs={'class':'form-control'}),
            'setup':forms.NumberInput(attrs={'class':'form-control'}),
            'carga_descarga':forms.NumberInput(attrs={'class':'form-control'}),
            'manutencao_corretiva':forms.NumberInput(attrs={'class':'form-control'}),
            'manutencao_preventiva':forms.NumberInput(attrs={'class':'form-control'}),
            'total_alvejado':forms.NumberInput(attrs={'class':'form-control'}),
            'total_chamuscado':forms.NumberInput(attrs={'class':'form-control'}),
            'total_expedido':forms.NumberInput(attrs={'class':'form-control'}),
            'total_recebido':forms.NumberInput(attrs={'class':'form-control'}),
            'total_tingido':forms.NumberInput(attrs={'class':'form-control'}),
        }
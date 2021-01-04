from django import forms
from .models import Producao, Material, Desempenho, Consumo, Custo, Perda
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
            'unidade': forms.Select(attrs={'class':'form-control'}),
        }


class CustoForm(forms.ModelForm):
    class Meta:
        model = Custo
        fields = (
            'periodo',
            'setor',                
            'energia',
            'laboratorio',            
            'manutencao',
            'mao_de_obra',
            'material_uso_continuo',
            'vapor',
            'agua',            
        )
        widgets = {                         
            'periodo': forms.HiddenInput(),
            'setor': forms.HiddenInput(),
            'energia':forms.NumberInput(attrs={'class':'form-control'}),            
            'laboratorio':forms.NumberInput(attrs={'class':'form-control'}),            
            'manutencao':forms.NumberInput(attrs={'class':'form-control'}),            
            'mao_de_obra':forms.NumberInput(attrs={'class':'form-control'}),            
            'material_uso_continuo':forms.NumberInput(attrs={'class':'form-control'}),            
            'vapor':forms.NumberInput(attrs={'class':'form-control'}),            
            'agua':forms.NumberInput(attrs={'class':'form-control'}),                        
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


class ConsumoModalForm(forms.ModelForm):
    class Meta:
        model = Consumo
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


class ConsumoForm(forms.ModelForm):
    class Meta:
        model = Consumo
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
        material_tipo = kwargs.pop('material_tipo', None)
        consumidos = kwargs.pop('consumidos', None)
        super().__init__(*args, **kwargs)

        self.fields['material'].queryset = self.fields['material'].queryset.filter(            
            tipo=material_tipo            
        ).order_by(
            'nome'
        ).exclude(
            id__in = consumidos
        )


class MaterialConsumoForm(forms.ModelForm):
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
            'origem': forms.Select(attrs={'class':'form-control'}),
            'tipo': forms.HiddenInput(),
            'unidade': forms.Select(attrs={'class':'form-control'}),
        }


class PerdaModalForm(forms.ModelForm):
    class Meta:
        model = Perda
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

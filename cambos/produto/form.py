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
        origem = kwargs.pop('origem', None)
        super().__init__(*args, **kwargs)

        self.fields['material'].queryset = self.fields['material'].queryset.filter(            
            tipo="Material",
            origem = origem
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
            'tempo_total_atendimento',            
        )
        widgets = {                         
            'periodo': forms.HiddenInput(),
            'setor': forms.HiddenInput(),
            'capacidade_total':forms.NumberInput(attrs={'class':'form-control'}),
            'dias_trabalhados':forms.NumberInput(attrs={'class':'form-control'}),
            'total_planejado':forms.NumberInput(attrs={'class':'form-control'}),
            'headcount':forms.NumberInput(attrs={'class':'form-control'}),
            'expedidores':forms.HiddenInput(),
            'revisores':forms.HiddenInput(),
            'setup':forms.NumberInput(attrs={'class':'form-control'}),
            'carga_descarga':forms.HiddenInput(),
            'manutencao_corretiva':forms.NumberInput(attrs={'class':'form-control'}),
            'manutencao_preventiva':forms.NumberInput(attrs={'class':'form-control'}),
            'total_alvejado':forms.HiddenInput(),
            'total_chamuscado':forms.HiddenInput(),
            'total_expedido':forms.HiddenInput(),
            'total_recebido':forms.HiddenInput(),
            'total_tingido':forms.HiddenInput(),
            'tempo_total_atendimento':forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        setor = kwargs.pop('setor', None)                
        super().__init__(*args, **kwargs)
        if setor == "Expedição":
            self.fields['expedidores'].widget = forms.NumberInput(attrs={'class':'form-control'})
            self.fields['total_recebido'].widget = forms.NumberInput(attrs={'class':'form-control'})
            self.fields['total_expedido'].widget = forms.NumberInput(attrs={'class':'form-control'})
            self.fields['carga_descarga'].widget = forms.NumberInput(attrs={'class':'form-control'})                  
        if setor == "Revisão":
            self.fields['revisores'].widget = forms.NumberInput(attrs={'class':'form-control'})                               
        if setor == "Acabamento":
            forms.Select(attrs={'class':'form-control'}),                             
            self.fields['total_alvejado'].widget = forms.NumberInput(attrs={'class':'form-control'})                              
            self.fields['total_tingido'].widget = forms.NumberInput(attrs={'class':'form-control'})                                         
        if setor == "Tecelagem":
            self.fields['tempo_total_atendimento'].widget = forms.NumberInput(attrs={'class':'form-control'})
            
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

    def __init__(self, *args, **kwargs):
        material_tipo = kwargs.pop('material_tipo', None)                
        super().__init__(*args, **kwargs)
        if material_tipo == "Insumo":
            self.fields['origem'].widget = forms.HiddenInput()            
            


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

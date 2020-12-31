from django import forms
from .models import Producao, Material
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
         
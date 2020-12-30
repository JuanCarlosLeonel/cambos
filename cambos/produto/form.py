from django import forms
from .models import Producao

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
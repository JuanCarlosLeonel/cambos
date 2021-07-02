

from django.forms import ModelForm, fields
from django import forms
from .models import Etapa, TAG


class EtapaForm(forms.ModelForm):
        class Meta:
            model = Etapa
            fields = ['processo', 'calendario', 'nome', 'interno', 'capacidade', 'linha', 'tag', 'nick_spi']

            widgets = {                         
                'nome': forms.TextInput(attrs={'class':'form-control'}),
                'calendario': forms.Select(attrs={'class':'form-control'}),
                'processo': forms.Select(attrs={'class':'form-control'}),
                'tag': forms.SelectMultiple(attrs={'class':'form-control'})
               
                }
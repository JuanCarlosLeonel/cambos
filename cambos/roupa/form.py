from django.forms import ModelForm, fields, widgets
from django import forms
from .models import Etapa, TAG, Pedido, PedidoTrack


class EtapaForm(forms.ModelForm):
        class Meta:
            model = Etapa
            fields = ['processo', 'calendario', 'nome', 'interno', 'capacidade', 'linha', 'score', 'tag', 'nick_spi']

            widgets = {                         
                'nome': forms.TextInput(attrs={'class':'form-control'}),
                'calendario': forms.Select(attrs={'class':'form-control'}),
                'processo': forms.Select(attrs={'class':'form-control'}),
                'tag': forms.SelectMultiple(attrs={'class':'form-control'})
               
                }


class TAGForm(forms.ModelForm):
    class Meta:
        model = TAG
        fields = ['nome']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['tag', 'lacre']

        widgets = {
            'tag': forms.SelectMultiple(attrs={'class':'form-control'}),
            'lacre': forms.HiddenInput(attrs={'class':'form-control'})
            
            }


import django_filters
from django_filters import DateFilter, CharFilter, ModelChoiceFilter, ChoiceFilter
from django import forms
from .models import Viagem, Pessoa, Motorista, Veiculo, Abastecimento
from django.db.models import Q
from django.db import models


class ViagemFilter(django_filters.FilterSet):
    veiculo = ModelChoiceFilter(queryset=Veiculo.objects.filter(caminhao=True),label='Veículo',widget=forms.Select(attrs={'class':'form-control'}))
    m = Motorista.objects.filter().values('nome')
    motorista = ModelChoiceFilter(queryset=Pessoa.objects.filter(id__in = m),widget=forms.Select(attrs={'class':'form-control'})) 
    motorista2 = ModelChoiceFilter(queryset=Pessoa.objects.filter(id__in = m),widget=forms.Select(attrs={'class':'form-control'}))
    ajudante = ModelChoiceFilter(queryset=Pessoa.objects.filter(status = 0),widget=forms.Select(attrs={'class':'form-control'}))
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data_inicial",label='Início')
    fim = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data_inicial",label='Fim')
    destino = CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}),field_name="destino",label='Destino',lookup_expr='icontains')
    q = CharFilter(method='my_custom_filter',label="MOTORISTA 1-2",widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Viagem
        fields = {
            'veiculo',
        }

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(motorista__nome__icontains=value) | Q(motorista2__nome__icontains=value)
        )


class ViagemFilterCarro(django_filters.FilterSet):
    veiculo = ModelChoiceFilter(queryset=Veiculo.objects.filter(caminhao=False),label='Veículo',widget=forms.Select(attrs={'class':'form-control'}))
    motorista = ModelChoiceFilter(queryset=Pessoa.objects.filter(status = 0),widget=forms.Select(attrs={'class':'form-control'}))
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data_inicial",label='Início')
    fim = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data_inicial",label='Fim')
    destino = CharFilter(widget=forms.TextInput(attrs={'class':'form-control'}),field_name="destino",label='Destino',lookup_expr='icontains')

    class Meta:
        model = Viagem
        fields = {
            'veiculo',
        }


class AbastecimentoFilter(django_filters.FilterSet):
    veiculo = ModelChoiceFilter(queryset=Veiculo.objects.filter(caminhao=False),label='Veículo',widget=forms.Select(attrs={'class':'form-control'}))
    combustivel = django_filters.ChoiceFilter(choices=Abastecimento.COMBUSTIVEL,label='Combustível',widget=forms.Select(attrs={'class':'form-control'}))
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data",label='Início')
    fim = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data",label='Fim')

    class Meta:
        model = Abastecimento
        fields = {
            'veiculo',
        }


class AbastecimentoFilterCaminhao(django_filters.FilterSet):
    veiculo = ModelChoiceFilter(queryset=Veiculo.objects.filter(caminhao=True),label='Veículo',widget=forms.Select(attrs={'class':'form-control'}))
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data",label='Início')
    fim = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type':'date','class':'form-control'}),field_name="data",label='Fim')

    class Meta:
        model = Abastecimento
        fields = {
            'veiculo',
            'interno',
        }
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }



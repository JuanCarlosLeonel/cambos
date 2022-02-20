import django_filters
from django_filters import DateFilter, BooleanFilter , CharFilter, ModelChoiceFilter, UUIDFilter
from django import forms
from .models import Viagem, Pessoa, Motorista, Veiculo

class ViagemFilter(django_filters.FilterSet):
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type': 'date'}),field_name="data_inicial",label='Início')
    fim = DateFilter(lookup_expr='lte',widget=forms.DateInput(attrs={'id': 'datepicker','type': 'date'}),field_name="data_inicial",label='Fim')
    
    m = Motorista.objects.filter().values('nome')
    motorista = ModelChoiceFilter(queryset=Pessoa.objects.filter(id__in = m),widget=forms.Select)
    veiculo = ModelChoiceFilter(queryset=Veiculo.objects.filter(caminhao=True),widget=forms.Select)
    class Meta:
        model = Viagem
        fields = {
            'veiculo',
            'motorista',
        }




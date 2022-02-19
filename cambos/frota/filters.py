import django_filters
from django_filters import DateFilter, BooleanFilter
from django import forms
from .models import *

class ViagemFilter(django_filters.FilterSet):
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type': 'date'}),field_name="data_inicial",label='Data Início')
    fim = DateFilter(lookup_expr='lte',widget=forms.DateInput(attrs={'id': 'datepicker','type': 'date'}),field_name="data_inicial",label='Data Fim')


    class Meta:
        model = Viagem
        fields = ['veiculo']




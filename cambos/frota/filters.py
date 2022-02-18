from cProfile import label
from cgitb import lookup
from dataclasses import field
import django_filters
from django_filters import DateFilter, BooleanFilter

from .models import *

class ViagemFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="data_criacao", lookup_expr='gte',label='Data Início')
    end_date = DateFilter(field_name="data_criacao", lookup_expr='lte',label='Data Fim')


    class Meta:
        model = Viagem
        fields = ['veiculo']
        exclude = ['data_criacao']




import django_filters
from django_filters import DateFilter, CharFilter, ModelChoiceFilter
from django import forms
from .models import Viagem, Pessoa, Motorista, Veiculo

class ViagemFilter(django_filters.FilterSet):
    veiculo = ModelChoiceFilter(queryset=Veiculo.objects.filter(caminhao=True),widget=forms.Select)
    m = Motorista.objects.filter().values('nome')
    motorista = ModelChoiceFilter(queryset=Pessoa.objects.filter(id__in = m),widget=forms.Select)
    motorista2 = ModelChoiceFilter(queryset=Pessoa.objects.filter(id__in = m),widget=forms.Select)
    ajudante = ModelChoiceFilter(queryset=Pessoa.objects.all(),widget=forms.Select)
    ajudante = ModelChoiceFilter(queryset=Pessoa.objects.all(),widget=forms.Select)
    inicio = DateFilter(lookup_expr='gte',widget=forms.DateInput(attrs={'id': 'datepicker','type': 'date'}),field_name="data_inicial",label='Início')
    fim = DateFilter(lookup_expr='lte',widget=forms.DateInput(attrs={'id': 'datepicker','type': 'date'}),field_name="data_inicial",label='Fim')
    destino = CharFilter(field_name="destino",label='Destino',lookup_expr='icontains')

    class Meta:
        model = Viagem
        fields = {
            'veiculo',
        }






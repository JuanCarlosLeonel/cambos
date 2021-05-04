from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil import parser
from collections import Counter
import collections


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'roupa/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = requests.get(
            'http://187.45.32.103:20080/spi/producaoservice/statusentrega'
        )
        dados = url.json()["value"]
        lista = []
        total_pecas = 0
        entrega_atraso = 0
        produto_parado = 0
        
        for produto in dados:
            decoder = parser.parse(produto['DataEntrega'])
            semana = datetime.isocalendar(decoder)[1]
            lista.append({
                
                'entrega':semana,
                'quantidade': produto['QuantPecas'],
                
            })
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado":
                entrega_atraso += 1
            if produto['Parado'] == "1":
                produto_parado += 1
        
        result = Counter()
        
        for i in lista:
            result [i['entrega']] += i['quantidade']
        result = collections.OrderedDict(sorted(result.items()))
        context['teste'] = list(result.keys())
        context['label'] = list(result.keys())
        context['value'] = list(result.values())
        context['total'] = total_pecas
        context['atrasado'] = entrega_atraso
        context['parado'] = produto_parado

        return context

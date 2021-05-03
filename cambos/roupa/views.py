from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil import parser

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'roupa/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = requests.get(
            url='http://187.45.32.103:20080/spi/producaoservice/statusentrega'
        )
        dados = url.json()["value"]
        lista = []
        for produto in dados:
            decoder = parser.parse(produto['DataEntrega'])
            semana = datetime.isocalendar(decoder)[1]
            lista.append({
                'FC': produto['FichaCorte'],
                'ENTREGA':semana,
                'QUANTIDADE': produto['QuantPecas']
            })
        
        context['dados'] = lista
        return context

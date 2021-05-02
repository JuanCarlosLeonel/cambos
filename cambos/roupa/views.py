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
            url='https://json.extendsclass.com/bin/9b619402741b'
        )
        dados = url.json()["ENTREGA"]
        lista = []
        for produto in dados:
            decoder = parser.parse(produto['ENTREGA'])
            semana = datetime.isocalendar(decoder)[1]
            lista.append({
                'FC': produto['FC'],
                'ENTREGA':semana,
                'QUANTIDADE': produto['QUANTIDADE']
            })
        
        context['dados'] = lista
        return context

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from dateutil import parser
from collections import Counter
import collections
import pandas as pd

def get_url():
    url = 'http://187.45.32.103:20080/spi/producaoservice/statusentrega'    
    dados = pd.read_json(url)
    return dados['value']

def convert_setor(id):
    lista = [
        "1.Modelagem",
        "2.Encaixe",
        "3.Expedição Tecido",
        "4.Corte",
        "5.Costura",
        "6.Finalização",
        "7.Lavanderia",
        "8.Qualidade",
        "9.Acabamento",
        "10.Expedição",
        "11.Pronto",
    ]
    nome = lista[id-1]
    return nome

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'roupa/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dados = get_url()
        lista = []
        total_pecas = 0
        entrega_atraso = 0
        quantidade_atraso = 0
        produto_parado = 0
        hoje = datetime.today()
        semana_atual = datetime.isocalendar(hoje)[1]+1
        for produto in dados:
            decoder = parser.parse(produto['DataEntrega'])
            semana_entrega = datetime.isocalendar(decoder)[1]+1            
            if semana_entrega < semana_atual:
                lista.append({
                    'em_dia': 0,
                    'em_atraso': 0,             
                    'entrega':semana_atual,                    
                })
            elif produto['Atrasado'] == "Em Atraso":
                lista.append({
                    'em_dia': 0,
                    'em_atraso': produto['QuantPecas'],                              
                    'entrega':semana_entrega,                    
                })
            else:
                lista.append({
                    'em_dia': produto['QuantPecas'],                
                    'em_atraso': 0,               
                    'entrega':semana_entrega,                    
                })
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado":
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
            if produto['Parado'] == "1":
                produto_parado += 1
        
        em_dia = Counter()
        em_atraso = Counter()
        atrasado = Counter()
        
        for i in lista:
            em_dia [i['entrega']] += i['em_dia']
            em_atraso [i['entrega']] += i['em_atraso']
           
        em_dia = collections.OrderedDict(sorted(em_dia.items()))
        em_atraso = collections.OrderedDict(sorted(em_atraso.items()))        
        context['semana_atual'] = semana_atual
        context['label'] = list(em_dia.keys())
        context['em_dia'] = list(em_dia.values())
        context['em_atraso'] = list(em_atraso.values())
        context['atrasado'] = quantidade_atraso
        context['total'] = total_pecas
        context['entrega_atraso'] = entrega_atraso
        context['parado'] = produto_parado  
        """d = dados.to_dict()    
        df=pd.DataFrame.from_dict(d, orient='index')  
        context['teste'] = df[df["Atrasado"]=="Em Dia"]"""

        return context


@method_decorator(login_required, name='dispatch')
class ProducaoRoupaList(TemplateView):    
    template_name = 'roupa/producao_roupa_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dados = get_url()
        for produto in dados:
            produto["Status"] = convert_setor(produto["Status"])
            produto["DataEntrega"] = parser.parse(produto['DataEntrega'])
        context['producaojs'] = dados
        context['teste'] = convert_setor(1)
        return context
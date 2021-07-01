import json
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
import requests
import json
from datetime import (datetime, timedelta, date)
from dateutil import parser
from collections import Counter
import collections
from .models import (
    Calendario,
    DiasCalendario,
    Etapa,    
    API 
    )
from django.http import JsonResponse
from dateutil.parser import parse


def update_api():
    url = 'http://187.45.32.103:20080/spi/intproducaoservice/statusentrega'
    response = requests.get(url)
    dados = response.json()
    model = API.objects.get(id=1)
    model.api = dados
    model.save()

def get_url():  
    try:  
        return  API.objects.get(id=1).api['value']
    except:
        url = 'http://187.45.32.103:20080/spi/intproducaoservice/statusentrega'
        response = requests.get(url)
        dados = response.json()
        return dados['value']


def convert_setor(id):
    lista = [
        "Modelagem",
        "Encaixe",
        "Expedição Tecido",
        "Corte",
        "Costura",
        "Finalização",
        "Lavanderia",
        "Qualidade",
        "Acabamento",
        "Expedição",
        "Pronto",
        "Geral",
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
                if produto['Status'] == 11:
                    lista.append({
                        'em_dia': 0,
                        'em_atraso': 0,                              
                        'estocado': produto['QuantPecas'],             
                        'entrega':semana_atual,                    
                    })
                else:
                    lista.append({
                        'em_dia': 0,
                        'em_atraso': 0,             
                        'estocado': 0,             
                        'entrega':semana_atual,                    
                    })
            elif produto['Status'] == 11:
                lista.append({
                    'em_dia': 0,
                    'em_atraso': 0,                              
                    'estocado': produto['QuantPecas'],             
                    'entrega':semana_entrega,                    
                })
            elif produto['Atrasado'] == "Em Atraso":
                lista.append({
                    'em_dia': 0,
                    'em_atraso': produto['QuantPecas'],                              
                    'estocado': 0,             
                    'entrega':semana_entrega,                    
                })
            else:
                lista.append({
                    'em_dia': produto['QuantPecas'],                
                    'em_atraso': 0,            
                    'estocado': 0,                
                    'entrega':semana_entrega,                    
                })
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado" and produto['Status'] != 11:
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
            if produto['Parado'] == "1" and produto['Status'] != 11:
                produto_parado += 1
        
        em_dia = Counter()
        em_atraso = Counter()
        estocado = Counter()
        
        for i in lista:
            em_dia [i['entrega']] += i['em_dia']
            em_atraso [i['entrega']] += i['em_atraso']
            estocado [i['entrega']] += i['estocado']
           
        em_dia = collections.OrderedDict(sorted(em_dia.items()))
        em_atraso = collections.OrderedDict(sorted(em_atraso.items()))        
        estocado = collections.OrderedDict(sorted(estocado.items()))        
        context['semana_atual'] = semana_atual
        context['label'] = list(em_dia.keys())
        context['em_dia'] = list(em_dia.values())
        context['em_atraso'] = list(em_atraso.values())
        context['estocado'] = list(estocado.values())
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
            produto["DataEntrega"] = parse(produto["DataEntrega"]).date()
        context['producaojs'] = dados        
        return context


@method_decorator(login_required, name='dispatch')
class CalendarioTemplate(TemplateView):
    template_name = 'roupa/calendario.html'

    def get(self, request, *args, **kwargs):     
        context = super().get_context_data(**kwargs)
        calendario = Calendario.objects.get(pk = self.kwargs['pk'])                           
        calendarios = Calendario.objects.filter()                           
        dados = DiasCalendario.objects.filter(calendario = self.kwargs['pk'])        
        lista = []
        for data in dados:            
            lista.append(str(f'{data.data} 0:0:0'))        
        context['calendarios'] = calendarios
        context['calendario'] = calendario
        context['dias'] = lista
        add = self.request.GET.get('adicionar')                 
        if not add is None:    
            list_add = list(add.split(","))  
            try:
                for c in list_add:        
                    date = c
                    model = DiasCalendario(calendario = calendario, data = date)                        
                    model.save()            
            except:
                pass
        deletar = self.request.GET.get('deletar')
        if not deletar is None:
            list_del = list(deletar.split(",")) 
            try:
                for c in list_del:
                    date = c
                    model = DiasCalendario.objects.filter(
                        calendario = calendario,
                        data = date
                    )
                    model.delete()            
            except:
                pass        
        if not add is None or not deletar is None:  
            return redirect(f'/roupa/calendario/{calendario.pk}')   
            
        else:
            return render(request, 'roupa/calendario.html', context)


@method_decorator(login_required, name='dispatch')
class ConfeccaoList(TemplateView):    
    template_name = 'roupa/confeccao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oficina_list = Etapa.objects.filter().order_by('nome')        
        dados = get_url()
        em_producao_int = []
        em_producao_ext = []
        for oficina in oficina_list:                        
            quant_un = 0
            quant_pt = 0
            contador = 0
            atraso = 0
            soma_duracao = 0
            for produto in dados:
                if oficina.nick_spi == produto["Celula"]:
                    dias = produto['DiasPedido'
                    ] + produto['DiasExpTecido'
                    ] + produto['DiasEncaixe'
                    ] + produto['DiasProducao']
                    
                    if produto["Status"] == 5:
                        if produto['Atrasado'] == "Em Atraso":
                            atraso +=1
                        contador += 1
                        quant_un += produto["QuantPecas"]
                        quant_pt += produto["ValorDentro"] * produto["QuantPecas"]
                        soma_duracao += produto["DiasCostura"]
            try:
                duracao = soma_duracao / contador
            except:
                duracao = 0
            if oficina.interno:
                em_producao_int.append({
                    'id': oficina.id,
                    'oficina': oficina.nome,
                    'quant_un':quant_un,
                    'quant_pt':quant_pt,
                    'duracao': duracao,
                    'contador': contador,
                    'dias':dias,
                    'em_atraso':atraso
                })
            else:
                em_producao_ext.append({
                    'id': oficina.id,
                    'oficina': oficina.nome,
                    'quant_un':quant_un,
                    'quant_pt':quant_pt,
                    'duracao': duracao,
                    'contador': contador,
                    'dias':dias,
                    'em_atraso':atraso
                })
                
        context['internas'] = em_producao_int
        context['externas'] = em_producao_ext
        context['teste'] = convert_setor(1)
        return context


@method_decorator(login_required, name='dispatch')
class ConfeccaoDetail(DetailView):    
    model = Etapa
    template_name = 'roupa/confeccao_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oficina = Etapa.objects.get(id = self.kwargs['pk'])        
        dados = get_url()        
        em_dia = []
        atrasado = []        
        parado =[]
        lista_intervalos = []
        produtos_em_linha = []
        calendario = DiasCalendario.objects.filter(calendario = oficina.calendario).order_by('data')
        data_inicial = ''        
        for item in calendario:            
            if data_inicial == "intervalo":
                final_intervalo= str(item.data - timedelta(days=1))
                lista_intervalos.append({'start':inicio_intervalo,'end':final_intervalo})
                data_inicial = item.data
            if data_inicial == '':
                data_inicial = item.data
            if item.data == data_inicial:
                data_inicial = item.data + timedelta(days=1)
            else:
                inicio_intervalo = str(data_inicial)
                data_inicial = "intervalo"
                        
        for produto in dados:
            if oficina.nick_spi == produto["Celula"]:                
                if produto["Status"] == 5:                                  
                    entrada = parse(produto["DataCostura"]).date()
                    produto['entrada'] = entrada
                    produtos_em_linha.append(produto)
            if oficina.nick_spi == "finalizacao":                
                if produto["Status"] == 6:                                  
                    entrada = parse(produto["DataFinalizacao"]).date()
                    produto['entrada'] = entrada
                    produtos_em_linha.append(produto)
        lista_ordenada = sorted(produtos_em_linha, key=lambda x: x['entrada'], reverse=False)
        ordem = 1
        soma_dias = 0
        capacidade = oficina.capacidade                         
        for produto in lista_ordenada:            
            quant_un = produto["QuantPecas"]
            if oficina.nick_spi == "finalizacao":                
                pont = produto["ValorReal"] - produto["ValorDentro"]
            else:
                pont = produto["ValorDentro"]
            quant_pt = pont * produto["QuantPecas"]             
            entrada = produto['entrada']
            duracao_estimada = round(quant_pt / capacidade) 
            entrada_calendario = calendario.filter(data__gte = entrada)
            entrega = entrada_calendario[1+ duracao_estimada + soma_dias].data
            if produto['Atrasado'] == "Em Atraso":
                situacao = "em_atraso"
            elif produto['Parado'] == "1":
                situacao = "parado"
            else:
                situacao = "em_dia"                        
            if entrega < date.today():
                dias_atraso = datetime.today()
            else:
                dias_atraso = ""

            linha = {                        
                'produto': produto["FichaCorte"],                    
                'quant_un':quant_un,
                'pont':pont,                
                'quant_pt':quant_pt,                        
                'dias':duracao_estimada,                                                   
                'entrada': str(entrada),                    
                'entrega': str(entrega),                                            
                'atraso': str(dias_atraso),                                            
                'situacao': situacao,                      
                'ordem':ordem,
                'soma_dias':soma_dias

            }
            if produto['Parado'] == "1":
                parado.append(linha)                    
            else:
                em_dia.append(linha)
                soma_dias += duracao_estimada
                ordem += 1                    
        lista = {'parado':parado, 'atrasado':atrasado, 'em_dia':em_dia}        
        context['lista'] = json.dumps(lista)
        context['intervalos'] = json.dumps(lista_intervalos)
        context['teste']= datetime.today()
        return context


@method_decorator(login_required, name='dispatch')
class ProgramacaoList(TemplateView):    
    template_name = 'roupa/programacao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dados = get_url()
        for produto in dados:
            produto["Status"] = convert_setor(produto["Status"])
            produto["DataEntrega"] = parse(produto["DataEntrega"]).date()
        context['producaojs'] = dados        
        return context

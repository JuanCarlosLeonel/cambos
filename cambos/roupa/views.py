import json
from django.http.response import HttpResponse

from requests.api import get
from .form import EtapaForm, PedidoForm, TAGForm
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
import requests
from datetime import (datetime, timedelta, date)
from dateutil import parser
from collections import Counter
import collections
from .models import (
    Calendario,
    DiasCalendario,
    Etapa,    
    API,
    PCP,
    Pedido,
    Processo,
    TAG,
    PedidoTrack,
    Track,
    RoupaBot
    )
from django.http import JsonResponse
from dateutil.parser import parse
from django.core import serializers


def parse_date(item):
    date = parse(item).date()
    return date


def get_etapa(pk):
    try:
        nome = Etapa.objects.get(pk = pk)
    except:
        nome = Etapa.objects.latest('id')
    return nome


def update_track(lacre):
    model = Track.objects.latest('pcp')
    pedido = PedidoTrack.objects.filter(lacre=lacre)
    try:
        for item in pedido:
            user = str(RoupaBot.objects.get(usuario = item.user).user_id)            
            model.pcp.append(
                {"lacre":lacre,
                "user":user
                }
            )
        model.save()
    except:
        pass


def update_api():
    try:
        url = 'http://187.45.32.235:20080/spi/intproducaoservice/statusentrega'
        response = requests.get(url)
        dados = response.json()
        model = API.objects.latest("id")
        model.api = dados
        model.save()
    except:
        pass


def get_url():  
    try:  
        return API.objects.latest("id").api['value']
    except:
        url = 'http://187.45.32.235:20080/spi/intproducaoservice/statusentrega'
        response = requests.get(url)
        dados = response.json()
        return dados['value']


def check_update_api():
    url = 'http://187.45.32.235:20080/spi/intproducaoservice/statusentrega'
    response = requests.get(url)
    dados_spi = response.json()
    dados_api = API.objects.latest("id").api
    dados_pcp = PCP.objects.latest("id")
    change_status = []
    new_api = []
    new_pcp = []
    old_api = []
    for item_spi in dados_spi['value']:        
        match_spi = 0        
        match_pcp = 0        
        for item_api in dados_api['value']:                        
            if item_spi['Lacre'] == item_api['Lacre']:                
                match_spi = 1
                if not item_spi['Status'] == item_api['Status']:                                        
                    change_status.append(item_spi['Lacre'])        
        if match_spi == 0:            
            new_api.append(item_spi['Lacre'])                    
        for item_pcp in dados_pcp.pcp:            
            if item_spi['Lacre'] == item_pcp['lacre']:
                match_pcp = 1
        if match_pcp == 0:
            new_pcp.append(item_spi['Lacre'])
    for item_api in dados_api['value']:
        match_api = 0
        for item_spi in dados_spi['value']:
            if item_api['Lacre'] == item_spi['Lacre']:
                match_api = 1
        if match_api == 0:
            old_api.append(item_api['Lacre'])

    if len(new_api) > 0 or len(change_status) > 0:
        update_api()        

    if len(change_status) > 0:        
        for item in change_status:
            update_track(item)
    
    if len(new_pcp) > 0:
        for item in new_pcp:
            novo = get_pcp_pedido(item)  
            if not novo == 0:                   
                dados_pcp.pcp.append(novo)            
                dados_pcp.save()    


def check_update_api2():
    url = 'http://187.45.32.235:20080/spi/intproducaoservice/statusentrega'
    response = requests.get(url)
    dados_spi = response.json()
    dados_api = API.objects.latest("id").api
    dados_pcp = PCP.objects.latest("id")
    change = 0    
    for item_spi in dados_spi['value']:
        match = 0
        for item_api in dados_api['value']:
            if item_spi['Lacre'] == item_api['Lacre']:                
                if not item_spi['Status'] == item_api['Status']:
                    update_api()
                    update_track(item_spi['Lacre'])
                    change = 1
        for item_pcp in dados_pcp.pcp:        
            if item_spi['Lacre'] == item_pcp['lacre']:
                match = 1                             
        if match == 0:                        
            change = 1
            novo = get_pcp_pedido(item_spi['Lacre'])  
            if not novo == 0:                   
                dados_pcp.pcp.append(novo)            
                dados_pcp.save()            

    if change == 1:
        update_api()        
    

def update_pcp(lacre):    
    dados_api = API.objects.latest("id").api
    dados_pcp = PCP.objects.latest("id")    
    for item_api in dados_api['value']:
        match = 0                
        for item_pcp in dados_pcp.pcp:        
            if item_api['Lacre'] == item_pcp['lacre']:
                match = 1                             
        if match == 0:                        
            novo = get_pcp_pedido(item_api['Lacre'])  
            if not novo == 0:                   
                dados_pcp.pcp.append(novo)            
                dados_pcp.save()            
    

def get_pcp_pedido(pk):
    try:        
        pcp = PCP.objects.latest("id").pcp      
        pedido = 0     
        for produto in pcp:        
            if produto['lacre'] == pk:                                
                pedido = produto      
        if pedido == 0 :
            dados = get_url()                    
            for produto in dados:
                if produto['Lacre']== pk:
                    pedido= {
                        "lacre": pk,                    
                        "pedido": produto['DataPedido'],                    
                        "entrega": produto['DataEntrega'],     
                        'programado': False,               
                        "processo": [
                            {
                                'nome':'Modelagem',
                                'p_inicio':produto['DataPedido'],                    
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=1)
                            },
                            {
                                'nome':'Expedição Tecido',
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=1),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=2)
                            },
                            {
                                'nome':'Encaixe',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=2),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=3)
                            },                            
                            {
                                'nome':'Corte',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=3),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=4)
                            },
                            {
                                'nome':'Costura',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=4),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=21)
                            },
                            {
                                'nome':'Lavanderia',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=21),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=24)
                            },
                            {
                                'nome':'Qualidade',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=24),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=25)
                            },
                            {
                                'nome':'Acabamento',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=25),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=28)
                            },
                            {
                                'nome':'Expedição',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=28),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=29)
                            },
                            {
                                'nome':'Estoque',                                
                                'p_inicio':parse_date(produto['DataPedido']) + timedelta(days=29),
                                'p_fim':parse_date(produto['DataPedido']) + timedelta(days=30)
                            },
                        ]
                    }                
    except:
        pedido = 0
    
    return pedido


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


def dados_pedido(lacre):
    dados = get_url()        
    lista = []    
    for produto in dados:
        if produto['Lacre']== lacre:
            lista = produto            
    return lista  


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
        ano_atual = datetime.isocalendar(hoje)[0]
        data_atual = int( str(ano_atual) + str(semana_atual).zfill(2))
        client_list = Counter()
        
        for produto in dados:            
            decoder = parser.parse(produto['DataEntrega'])
            semana_entrega = datetime.isocalendar(decoder)[1]+1            
            ano_entrega = datetime.isocalendar(decoder)[0]
            data_entrega = int(str(ano_entrega) + str(semana_entrega).zfill(2))        
            if data_entrega < data_atual:
                if produto['Status'] >= 10:
                    lista.append({
                        'em_dia': 0,
                        'em_atraso': 0,                              
                        'estocado': produto['QuantPecas'],             
                        'entrega':semana_atual,                    
                        'ordem':data_atual
                    })
                else:
                    lista.append({
                        'em_dia': 0,
                        'em_atraso': 0,             
                        'estocado': 0,             
                        'entrega':semana_atual,                    
                        'ordem':data_atual
                    })
            elif produto['Status'] >= 10:
                lista.append({
                    'em_dia': 0,
                    'em_atraso': 0,                              
                    'estocado': produto['QuantPecas'],             
                    'entrega':semana_entrega,                    
                    'ordem':data_entrega
                })
            elif produto['Atrasado'] == "Em Atraso":
                lista.append({
                    'em_dia': 0,
                    'em_atraso': produto['QuantPecas'],                              
                    'estocado': 0,             
                    'entrega':semana_entrega,                    
                    'ordem':data_entrega
                })
            else:
                lista.append({
                    'em_dia': produto['QuantPecas'],                
                    'em_atraso': 0,            
                    'estocado': 0,                
                    'entrega':semana_entrega,                    
                    'ordem':data_entrega
                })
            total_pecas += produto['QuantPecas']
            if produto['Atrasado'] == "Atrasado" and produto['Status'] < 10:
                entrega_atraso += 1
                quantidade_atraso += produto['QuantPecas']
            if produto['Parado'] == "1" and produto['Status'] < 10:
                produto_parado += 1
        
            client_list [produto['Nome']] += produto['QuantPecas']
        
        em_dia = Counter()
        em_atraso = Counter()
        estocado = Counter()
        newlist = sorted(lista, key=lambda d: d['ordem']) 
        client_list = collections.OrderedDict(client_list.most_common())
        for i in newlist:
            em_dia [i['entrega']] += i['em_dia']
            em_atraso [i['entrega']] += i['em_atraso']
            estocado [i['entrega']] += i['estocado']
           
             
        context['semana_atual'] = semana_atual
        context['label'] = list(em_dia.keys())
        context['em_dia'] = list(em_dia.values())
        context['em_atraso'] = list(em_atraso.values())
        context['estocado'] = list(estocado.values())
        context['atrasado'] = quantidade_atraso
        context['total'] = total_pecas
        context['entrega_atraso'] = entrega_atraso
        context['parado'] = produto_parado  
        context['clientes_label'] = list(client_list.keys())
        context['clientes_quant'] = list(client_list.values())

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
                        elif produto['DiasCostura'] >=18:
                            atraso +=1
                        contador += 1
                        quant_un += produto["QuantPecas"]
                        quant_pt += produto["ValorDentro"] * produto["QuantPecas"]
                        soma_duracao += produto["DiasCostura"]
                elif oficina.nick_spi == "finalizacao":                
                    if produto["Status"] == 6:  
                        if produto['Atrasado'] == "Em Atraso":
                            atraso +=1
                        elif produto['DiasCostura'] >= 18:
                            atraso +=1
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
            produto["QuantPecas"] = produto["QuantPecas"]
        context['producaojs'] = dados        
        return context


@method_decorator(login_required, name='dispatch')
class PedidoDetail(TemplateView):    
    template_name = 'roupa/pedido_detail.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)                        
        lacre = self.kwargs['pk']
        lista = dados_pedido(lacre)   
        context['pedido'] = lista
        try:     
            pedido_tag=Pedido.objects.get(lacre=self.kwargs['pk'])
        except:
            pedido_tag=0
        context['pedido_tag'] = pedido_tag
        pcp = get_pcp_pedido(lacre)        
        for item in pcp['processo']:
            item['inicio'] = ""           
            item['fim'] = ""      
            if item['nome'] == "Modelagem":
                if not lista['DataPedido'] is None:
                    item['inicio'] = lista['DataPedido']                   
                    if not lista['DataExpTecido'] is None:
                        item['fim'] = lista['DataExpTecido']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Expedição Tecido":
                if not lista['DataExpTecido'] is None:
                    item['inicio'] = lista['DataExpTecido']                   
                    if not lista['DataEncaixe'] is None:
                        item['fim'] = lista['DataEncaixe']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Encaixe":
                if not lista['DataEncaixe'] is None:
                    item['inicio'] = lista['DataEncaixe']                   
                    if not lista['DataProducao'] is None:
                        item['fim'] = lista['DataProducao']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Corte":
                if not lista['DataProducao'] is None:
                    item['inicio'] = lista['DataProducao']                   
                    if not lista['DataCostura'] is None:
                        item['fim'] = lista['DataCostura']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Costura":
                if not lista['DataCostura'] is None:
                    item['inicio'] = lista['DataCostura']                   
                    if not lista['DataLavanderia'] is None:
                        item['fim'] = lista['DataLavanderia']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Lavanderia":
                if not lista['DataLavanderia'] is None:
                    item['inicio'] = lista['DataLavanderia']                   
                    if not lista['DataQualidade'] is None:
                        item['fim'] = lista['DataQualidade']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Qualidade":
                if not lista['DataQualidade'] is None:
                    item['inicio'] = lista['DataQualidade']                   
                    if not lista['DataAcabamento'] is None:
                        item['fim'] = lista['DataAcabamento']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Acabamento":
                if not lista['DataAcabamento'] is None:
                    item['inicio'] = lista['DataAcabamento']                   
                    if not lista['DataExpedicao'] is None:
                        item['fim'] = lista['DataExpedicao']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Expedição":
                if not lista['DataExpedicao'] is None:
                    item['inicio'] = lista['DataExpedicao']                   
                    if not lista['DataFimProducao'] is None:
                        item['fim'] = lista['DataFimProducao']
                    else:
                        item['fim'] = str(datetime.today())
            if item['nome'] == "Estoque":
                if not lista['DataFimProducao'] is None:
                    item['inicio'] = lista['DataFimProducao']                                           
                    item['fim'] = str(datetime.today())

        context['programacao'] = json.dumps(pcp)
        usuario = self.request.user
        listarastreado = PedidoTrack.objects.filter(user=usuario,lacre=lacre)
        rastreado = len(listarastreado)
        context['rastreio'] = rastreado
        edit = self.request.GET.get('editar') 
        if edit == 'true':
            model = PedidoTrack(user = usuario, lacre = lacre)
            model.save()

        elif edit == 'false':
            model = PedidoTrack.objects.get(user=usuario,lacre=lacre)
            model.delete()

        if not edit is None :  
            return redirect(f'/roupa/pedido_detail/{lacre}')   
            
        else:
            return render(request, 'roupa/pedido_detail.html', context)


@method_decorator(login_required, name='dispatch')
class PedidoCreate(CreateView):    
    model = Pedido
    template_name = 'roupa/pedido_create.html'
    form_class = PedidoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dados = get_url()        
        lista = []
        tags = TAG.objects.filter()
        
        for produto in dados:
            if produto['Lacre']== self.kwargs['pk']:
                try:
                    pedido = Pedido.objects.get(lacre=produto['Lacre'])
                except:
                    pedido = False
                lista = produto
        context['object'] = pedido            
        context['dados'] = lista        
        context['tags'] = tags            
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        return f'/roupa/pedido_detail/{pk}'

    def get_initial(self, *args, **kwargs):
        initial = super(PedidoCreate, self).get_initial(**kwargs)
        lacre = self.kwargs['pk']
        initial['lacre'] = lacre
        return initial


@method_decorator(login_required, name='dispatch')
class PedidoUpdate(UpdateView):    
    model = Pedido
    template_name = 'roupa/pedido_update.html'
    form_class = PedidoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dados = get_url()        
        lista = []
        tags = TAG.objects.filter()
        pedido= False
        lacre = self.kwargs['pk']
        for produto in dados:
            if produto['Lacre']== lacre:
                try:
                    pedido = Pedido.objects.get(lacre=produto['Lacre'])
                except:
                    pedido = False
                lista = produto
        context['object'] = pedido            
        context['dados'] = lista        
        context['tags'] = tags            
        return context

    def get_success_url(self):
        pk = self.object.lacre
        return f'/roupa/pedido_detail/{pk}'


@method_decorator(login_required,name='dispatch')
class PedidoUpdateTag(CreateView):
    form_class = TAGForm
    template_name = 'roupa/tag_create.html'
    model = TAG

    def get_success_url(self):
        pk = self.kwargs['pk']
        return f'/roupa/pedido_update/{pk}'


@method_decorator(login_required, name='dispatch')
class CreateOficina(CreateView):
    form_class = EtapaForm
    template_name = 'roupa/oficina_create.html'
    model = Etapa

    def get_success_url(self):
        return '/roupa/confeccao_list' 


@method_decorator(login_required, name='dispatch')
class UpdateOficina(UpdateView):
  model = Etapa
  template_name = 'roupa/oficina_update.html'
  form_class = EtapaForm

  def get_success_url(self):
      pk = self.kwargs['pk']
      return f'/roupa/confeccao_detail/{pk}'


@method_decorator(login_required, name='dispatch')
class TagCreate(CreateView):
    form_class = TAGForm
    template_name = 'roupa/tag_create.html'
    model = TAG

    def get_success_url(self):
        pk = self.kwargs['pk']
        return f'/roupa/oficina_update/{pk}'

 
@method_decorator(login_required, name='dispatch')
class ListPcpUpdate(TemplateView):    
    template_name = 'roupa/pcp_update.html'

    def get(self, request, *args, **kwargs):     
        context = super().get_context_data(**kwargs)
        dados = get_url()        
        pk = self.kwargs['pk']
        pcp = get_pcp_pedido(pk)
        for produto in dados:
            if produto['Lacre']== pk:
                produto['Status']=convert_setor(produto['Status'])                
                pedido = produto
        
        context['pedido'] = json.dumps(pedido)
        context['pcp'] = json.dumps(pcp)
        dict_obj = serializers.serialize('json',Processo.objects.filter())
        context['processo'] = dict_obj
        
        edit = self.request.GET.get('editar')                 
        if not edit is None:                
            pedido = json.loads(edit)
            model = PCP.objects.latest("id")
            novo = 0
            cont = 0
            for item in model.pcp:
                if item['lacre'] == pk:
                    model.pcp[cont] = pedido
                    novo = 1
                cont += 1
            if novo == 0:
                model.pcp.append(pedido)
            
            model.save()
            
        if not edit is None:  
            return redirect(f'/roupa/pedido_detail/{pk}')   
            
        else:
            return render(request, 'roupa/list_pcp_update.html', context)


@method_decorator(login_required, name='dispatch')
class PcpUpdate(TemplateView):    
    template_name = 'roupa/pcp_update.html'

    def get(self, request, *args, **kwargs):     
        context = super().get_context_data(**kwargs)             
        pk = self.kwargs['pk']
        pcp = get_pcp_pedido(pk)
        pedido = dados_pedido(pk)
        pedido['Status']=convert_setor(pedido['Status'])                
        pcp['pedido'] = parse(pcp["pedido"]).date()
        pcp['entrega'] = parse(pcp["entrega"]).date()
        context['pedido'] = json.dumps(pedido)
        context['pcp'] = pcp

        processo = self.kwargs['pk2']
        etapa_list = []
        if processo == "Costura":
            etapa_list = Etapa.objects.filter(
                processo__nome = "Costura"
                ).exclude(nome = "Finalização"
                ).order_by('-interno','nome')
        context['etapa_list'] = etapa_list

        edit = self.request.GET.get('editar')                 
        if not edit is None:                
            pedido = json.loads(edit)
            model = PCP.objects.latest("id")
            novo = 0
            cont = 0
            for item in model.pcp:
                if item['lacre'] == pk:
                    model.pcp[cont] = pedido
                    novo = 1
                cont += 1
            if novo == 0:
                model.pcp.append(pedido)
            
            model.save()
            
        if not edit is None:  
            return redirect(f'/roupa/pedido_detail/{pk}')   
            
        else:
            return render(request, 'roupa/pcp_update.html', context)


@method_decorator(login_required, name='dispatch')
class PcpList(TemplateView):    
    template_name = 'roupa/pcp_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)            
        pk = self.kwargs['pk']
        pcp = get_pcp_pedido(pk)
        pedido = dados_pedido(pk)
        for item in pcp['processo']:
            item['inicio'] = ""           
            item['fim'] = ""      
            if item['nome'] == "Modelagem":
                if not pedido['DataPedido'] is None:
                    item['inicio'] = parse_date(pedido['DataPedido'])
                    item['p_fim'] = parse_date(item['p_fim'])
                    if not pedido['DataExpTecido'] is None:
                        item['fim'] = parse_date(pedido['DataExpTecido'])                    
            if item['nome'] == "Expedição Tecido":
                if not pedido['DataExpTecido'] is None:
                    item['inicio'] = parse_date(pedido['DataExpTecido'])
                    if not pedido['DataEncaixe'] is None:
                        item['fim'] = parse_date(pedido['DataEncaixe'])                   
            if item['nome'] == "Encaixe":
                if not pedido['DataEncaixe'] is None:
                    item['inicio'] = parse_date(pedido['DataEncaixe'])
                    if not pedido['DataProducao'] is None:
                        item['fim'] = parse_date(pedido['DataProducao'])                   
            if item['nome'] == "Corte":
                if not pedido['DataProducao'] is None:
                    item['inicio'] = parse_date(pedido['DataProducao'])
                    if not pedido['DataCostura'] is None:
                        item['fim'] = parse_date(pedido['DataCostura'])
            if item['nome'] == "Costura":
                if not pedido['DataCostura'] is None:
                    item['inicio'] = parse_date(pedido['DataCostura'])                   
                    if not pedido['DataLavanderia'] is None:
                        item['fim'] = parse_date(pedido['DataLavanderia'])
            if item['nome'] == "Lavanderia":
                if not pedido['DataLavanderia'] is None:
                    item['inicio'] = parse_date(pedido['DataLavanderia'])                   
                    if not pedido['DataQualidade'] is None:
                        item['fim'] = parse_date(pedido['DataQualidade'])
            if item['nome'] == "Qualidade":
                if not pedido['DataQualidade'] is None:
                    item['inicio'] = parse_date(pedido['DataQualidade'])                   
                    if not pedido['DataAcabamento'] is None:
                        item['fim'] = parse_date(pedido['DataAcabamento'])
            if item['nome'] == "Acabamento":
                if not pedido['DataAcabamento'] is None:
                    item['inicio'] = parse_date(pedido['DataAcabamento'])                   
                    if not pedido['DataExpedicao'] is None:
                        item['fim'] = parse_date(pedido['DataExpedicao'])
            if item['nome'] == "Expedição":
                if not pedido['DataExpedicao'] is None:
                    item['inicio'] = parse_date(pedido['DataExpedicao'])                   
                    if not pedido['DataFimProducao'] is None:
                        item['fim'] = parse_date(pedido['DataFimProducao'])
            if item['nome'] == "Estoque":
                if not pedido['DataFimProducao'] is None:
                    item['inicio'] = parse_date(pedido['DataFimProducao'])
                    item['fim'] = str(datetime.today())
        pedido['Status']=convert_setor(pedido['Status'])                
        pcp['pedido'] = parse_date(pcp["pedido"])
        pcp['entrega'] = parse_date(pcp["entrega"])
        context['pedido'] = json.dumps(pedido)
        context['pcp'] = pcp                
        context['lacre'] = pk
        return context
        

class LogSuccessResponse(HttpResponse):

    def close(self):
        super(LogSuccessResponse, self).close()
        if self.status_code == 200:            
            update_api()
            update_track(self.content)


def UpdateAPI(request, pk):
    response = LogSuccessResponse(pk)
    return response



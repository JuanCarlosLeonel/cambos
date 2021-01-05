from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.models import Setor, Periodo, User
from produto.models import (
    Producao,
    Desempenho,
    Custo,
    Perda,
    Material,
    Consumo,
    ValorCompra,
    Custo
)
from core.form import UserCreationForm
from django.db.models import Sum, Count
import json
from django.core import serializers
from django.http import JsonResponse
from django.urls import reverse_lazy


class UserCreate(CreateView):     
    model = User
    form_class = UserCreationForm
    
    def get_success_url(self):
        return reverse_lazy('core_index')


def get_periodo(self):
    try:
        periodo = Periodo.objects.get(nome = self.request.GET.get('periodo', None))
    except:
        periodo = Periodo.objects.latest('periodo')
    return periodo

def get_setor(self):
    try:
        setor = Setor.objects.get(id = self.request.GET.get('setor', None))
    except:
        setor = Setor.objects.get(id=7)
    return setor

def producao_setor(id_setor, id_periodo):
    producao = Producao.objects.filter(
        setor = id_setor,
        periodo = id_periodo
    )    
    return producao

def perda_setor(id_setor, id_periodo):
    perda = Perda.objects.filter(
        setor = id_setor,
        periodo = id_periodo
    )    
    return perda

def custo_setor(id_setor, id_periodo):
    try:
        custo = Custo.objects.get(
            setor = id_setor,
            periodo = id_periodo
        )
    except:
        custo = Custo.objects.filter(setor = id_setor).latest('periodo')
    custo_total = custo.energia + custo.laboratorio + custo.manutencao + custo.material_uso_continuo + custo.mao_de_obra + custo.vapor + custo.agua
    return custo, custo_total

def compra_setor(id_setor, id_periodo):
    lista = []
    consumo = Consumo.objects.filter(
        setor = id_setor,
        periodo = id_periodo,
        material__origem = "Compra",        
    )
    total_insumo = 0
    total_material = 0
    for item in consumo:        
        try:
            preco = ValorCompra.objects.get(material__id = item.material.id, periodo = id_periodo).valor
        except:
            try:
                preco = ValorCompra.objects.filter(material__id = item.material.id).latest('periodo').valor
            except:
                preco = 0
        lista.append({
            'tipo':item.material.tipo,
            'material':item.material,
            'quantidade':item.quantidade,
            'valor': preco,
            'total': preco * item.quantidade
        })
        if item.material.tipo == "Insumo":
            total_insumo += preco * item.quantidade
        elif item.material.tipo == "Material":
            total_material += preco * item.quantidade

    return lista, total_insumo, total_material

def preco_material(id_material, periodo):
    preco = 0
    material = Material.objects.get(
        id = id_material
    )                        
    if material.origem == "Compra":
        historico_compra = ValorCompra.objects.filter(material = material).aggregate(
            Count('id'))['id__count']
        if historico_compra == 0:
            preco = 0
        else:      
            try:
                preco = ValorCompra.objects.get(
                    material = material,
                    periodo = periodo.id
                ).valor
            except:
                ultima_compra = ValorCompra.objects.filter(material = material).latest('periodo').valor
                preco = ultima_compra
    else:
        setor = Setor.objects.get(nome = material.origem)
        consumo = Consumo.objects.filter(
            material__origem = "Compra",
            periodo = periodo.id,
            setor = setor.id
        )
        consumo_total = 0
        for produto in consumo:
            historico_compra = ValorCompra.objects.filter(material = produto.material).aggregate(
            Count('id'))['id__count']
            if historico_compra == 0:
                preco = 0
            else:      
                try:
                    preco = ValorCompra.objects.get(
                        material = produto.material,
                        periodo = periodo.id
                    ).valor
                except:
                    ultima_compra = ValorCompra.objects.filter(material = produto.material).latest('periodo').valor
                    preco = ultima_compra            
            consumo_total += preco * produto.quantidade            
        producao = producao_setor(setor.id, periodo.id).aggregate(
            Sum('quantidade'))['quantidade__sum']        
        custo = custo_setor(setor.id, periodo.id)[1]
        try:
            preco = (custo + consumo_total) / producao
        except:
            preco = 0    
    return preco

def label(nome_periodo, id_periodo, id_setor):
    ano = int(nome_periodo[len(nome_periodo)-4:])
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    meses_abr = ["Jan", "fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    periodo_ind = meses_abr.index(nome_periodo[0:3])
    if periodo_ind == 11:
        p_inicio = 0
    else:
        p_inicio = periodo_ind + 1
    p_fim = 0
    id_periodo -= 11
    label_periodo = []
    data = []
    while (p_fim < 12):
        p_fim += 1
        label_periodo.append(meses_abr[p_inicio])
        try:
            producao = producao_setor(id_setor, id_periodo).aggregate(
                Sum('quantidade'))['quantidade__sum']
            if not producao:
                producao = 0
        except:
            producao = 0
        data.append(int(producao))
        id_periodo += 1
        if p_inicio == 11:
            p_inicio = 0
        else:
            p_inicio += 1
    else:
        return label_periodo, data

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)

        producao = producao_setor(setor.id, periodo.id).aggregate(
            Sum('quantidade'))['quantidade__sum']

        if setor.id < 5:
            unidades = 'Quilos'
            unidade = 'Quilo'
        else:
            unidades = 'Metros'
            unidade = 'Metro'
        
        try:
            total_planejado = Desempenho.objects.get(
                setor = setor.id,
                periodo = periodo.id
            ).total_planejado
        except:
            total_planejado = 0

        try:
            eficiencia = (producao / total_planejado) * 100
        except:
            eficiencia = 0
        try:
            custo = custo_setor(setor.id, periodo.id)[1]                
            custo_un = custo / producao
        except:
            custo_un = 0
        perda = perda_setor(setor.id, periodo.id).aggregate(
            Sum('quantidade'))['quantidade__sum']        
        try:
            perda_un = (perda / producao) * 100
        except:
            perda_un = 0

        insumo = compra_setor(setor.id, periodo.id)[1]
        try:
            insumo_un = insumo / producao
        except:
            insumo_un = 0
        
        valor_consumo_material = compra_setor(setor.id, periodo.id)[2]        
        try:
            materia_prim_un = valor_consumo_material / producao
        except:
            materia_prim_un = 0
        materia_prima = materia_prim_un
                
        context['data'] = label(periodo.nome, periodo.id, setor.id)[1]    
        context['labels'] = label(periodo.nome, periodo.id, setor.id)[0]    
        context['materia_prima'] = materia_prima
        context['insumo'] = insumo_un
        context['perda'] = perda_un
        context['custo'] = custo_un
        context['eficiencia'] = eficiencia
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = producao
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class ProducaoList(ListView):
    model= Producao
    template_name = 'core/producao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        producao = producao_setor(setor.id, periodo.id)
        total = producao.aggregate(
            Sum('quantidade'))['quantidade__sum']
        if setor.id < 5:
            unidades = 'Quilos'
            unidade = 'kg'
        else:
            unidades = 'Metros'
            unidade = 'm'
        lista = []  
        if setor.id < 5:
            origem = setor.nome
        else:
            origem = "Tecelagem"
        historico = Material.objects.filter(
            origem = origem            
        ).order_by('nome')
        for material in historico:
            material_nome = material.nome
            quantidade = 0
            percentual = 0    
            id_producao = ''
            id_material = material.id
            for item in producao.distinct('material'):
                if item.material.id == material.id:
                    quantidade = item.quantidade
                    percentual = (item.quantidade / total)*100
                    id_producao = item.id
            if material.inativo and quantidade == 0:
                pass
            else:                    
                lista.append({                
                    'material': material_nome,
                    'quantidade': quantidade,
                    'percentual': percentual,
                    'id': id_producao,                
                    'id_material': id_material                
                    })
                        
        context['historico'] = historico
        context['producaojs'] = sorted(lista, key=lambda x: x['quantidade'], reverse=True)
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = total
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class PerdaList(ListView):
    model= Perda
    template_name = 'core/perda_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        perda = perda_setor(setor.id, periodo.id)
        total = perda.aggregate(
            Sum('quantidade'))['quantidade__sum']
        if setor.id < 5:
            unidades = 'Quilos'
            unidade = 'kg'
        else:
            unidades = 'Metros'
            unidade = 'm'
        lista = []          
        historico = Perda.objects.filter(
            setor = setor.id,            
        ).distinct('material')
        for material in historico:
            material_nome = material.material.nome
            quantidade = 0
            percentual = 0    
            id_perda = ''
            id_material = material.material.id
            for item in perda.distinct('material'):
                if item.material.id == material.material.id:
                    quantidade = item.quantidade
                    percentual = (item.quantidade / total)*100
                    id_perda = item.id
            if material.material.inativo and quantidade == 0:
                pass
            else:                    
                lista.append({                
                    'material': material_nome,
                    'quantidade': quantidade,
                    'percentual': percentual,
                    'id': id_perda,                
                    'id_material': id_material                
                    })                                
        context['producaojs'] = sorted(lista, key=lambda x: x['quantidade'], reverse=True)
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = total
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context



@method_decorator(login_required, name='dispatch')
class ConsumoMaterialList(ListView):
    model= Consumo
    template_name = 'core/consumo_material_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        consumo = Consumo.objects.filter(
            setor = setor.id,
            periodo = periodo.id,            
            material__tipo = "Material"            
        )        
        lista = []          
        historico = Consumo.objects.filter(
            setor = setor.id,
            material__tipo = "Material"            
        ).distinct('material')
        

        quantidade = 0
        preco = 0
        total = 0  
        valor = 0                               
        for consumido in consumo:
            quantidade = consumido.quantidade           
            preco = preco_material(consumido.material.id, periodo)                
            valor = quantidade * preco                    
            total += valor                   
            
        for item in historico:
            material_nome = item.material.nome
            origem = item.material.origem
            quantidade = 0            
            preco = preco_material(item.material.id, periodo)            
            percentual = 0    
            id_consumo = ''
            id_material = item.material.id
            valor = 0
            
            for consumido in consumo:
                if consumido.material.id == item.material.id:
                    quantidade = consumido.quantidade                    
                    valor = quantidade * preco
                    try:                        
                        percentual = (valor / total) * 100                        
                    except:
                        percentual = 0                        
                    id_consumo = consumido.id
            if item.material.inativo and quantidade == 0:
                pass
            else:                    
                lista.append({                
                    'material': material_nome,
                    'origem': origem,
                    'quantidade': quantidade,
                    'preco': preco,
                    'percentual': percentual,
                    'valor': valor,
                    'id': id_consumo,                
                    'id_material': id_material                
                    })
                        
        context['historico'] = historico
        context['producaojs'] = sorted(lista, key=lambda x: x['valor'], reverse=True)        
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class ConsumoInsumoList(ListView):
    model= Consumo
    template_name = 'core/consumo_insumo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        consumo = Consumo.objects.filter(
            setor = setor.id,
            periodo = periodo.id,            
            material__tipo = "Insumo",            
        )        
        lista = []          
        historico = Consumo.objects.filter(
            setor = setor.id,
            material__tipo = "Insumo",            
        ).distinct('material')        
        quantidade = 0
        preco = 0
        total = 0  
        valor = 0                               
        for consumido in consumo:
            quantidade = consumido.quantidade           
            preco = preco_material(consumido.material.id, periodo)                
            valor = quantidade * preco                    
            total += valor                   
            
        for item in historico:
            material_nome = item.material.nome            
            quantidade = 0            
            preco = preco_material(item.material.id, periodo)            
            percentual = 0    
            id_consumo = ''
            id_material = item.material.id
            valor = 0
            
            for consumido in consumo:
                if consumido.material.id == item.material.id:
                    quantidade = consumido.quantidade                    
                    valor = quantidade * preco
                    try:                        
                        percentual = (valor / total) * 100                        
                    except:
                        percentual = 0                        
                    id_consumo = consumido.id
            if item.material.inativo and quantidade == 0:
                pass
            else:                    
                lista.append({                
                    'material': material_nome,                    
                    'quantidade': quantidade,
                    'preco': preco,
                    'percentual': percentual,
                    'valor': valor,
                    'id': id_consumo,                
                    'id_material': id_material                
                    })
                        
        context['historico'] = historico
        context['producaojs'] = sorted(lista, key=lambda x: x['valor'], reverse=True)        
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class DesempenhoList(ListView):
    model= Desempenho
    template_name = 'core/desempenho_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        if setor.id < 5:            
            unidade_prod = 'kilos'
        else:            
            unidade_prod = 'metros'
        lista = []
        opcoes= (
            {'item':'capacidade_total',
            'nome':'Capacidade Total',
            'un': unidade_prod},
            {'item':'dias_trabalhados',
            'nome':'Dias Trabalhados',
            'un': 'dias'},
            {'item':'headcount',
            'nome':'Colaboradores',
            'un': 'Pessoas'},
            {'item':'expedidores',
            'nome':'Expedidores',
            'un': 'Pessoas'},
            {'item':'revisores',
            'nome':'Revisores',
            'un': 'Pessoas'},
            {'item':'setup',
            'nome':'Setup',
            'un': 'horas'},
            {'item':'carga_descarga',
            'nome':'Carga e descarga',
            'un': 'horas'},
            {'item':'manutencao_corretiva',
            'nome':'Manutenção Corretiva',
            'un': 'horas'},
            {'item':'manutencao_preventiva',
            'nome':'Manutenção Preventiva',
            'un': 'horas'},
            {'item':'total_alvejado',
            'nome':'Total Alvejado',
            'un': unidade_prod},
            {'item':'total_chamuscado',
            'nome':'Total Chamuscado',
            'un': unidade_prod},            
            {'item':'total_expedido',
            'nome':'Total Expedido',
            'un': unidade_prod},
            {'item':'total_recebido',
            'nome':'Total Recebido',
            'un': unidade_prod},
            {'item':'total_tingido',
            'nome':'Total Tingido',
            'un': unidade_prod},
        )        
        try:                   
            desempenho = Desempenho.objects.get(
                periodo = periodo.id,
                setor = setor.id
            )        
            lancado = desempenho.pk
        except:
            desempenho = ''
            lancado = False
        for opcao in opcoes:
            item = opcao['nome']
            if desempenho:
                valor = getattr(desempenho, opcao['item'])
            else:
                valor = 0
            if valor is None:
                valor = 0
            else:
                valor = int(valor)
            un = opcao['un']
            lista.append({'item':item, 'valor':valor, 'un':un})                               
        context['lancado'] = lancado
        context['data'] = lista
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
        

@method_decorator(login_required, name='dispatch')
class CustoList(ListView):
    model= Custo
    template_name = 'core/custo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        
        lista = []
        opcoes= (                
            {'item':'energia',
            'nome':'Energia',
            },
            {'item':'laboratorio',
            'nome':'Laboratório',
            },
            {'item':'manutencao',
            'nome':'Manutenção',
            },
            {'item':'mao_de_obra',
            'nome':'Mão de Obra',
            },
            {'item':'material_uso_continuo',
            'nome':'Material de Uso Contínuo',
            },
            {'item':'vapor',
            'nome':'Vapor',
            },
            {'item':'agua',
            'nome':'Água',
            },            
        )        
        try:                   
            custo = Custo.objects.get(
                periodo = periodo.id,
                setor = setor.id
            )        
            lancado = custo.pk
        except:
            custo = ''
            lancado = False
        for opcao in opcoes:
            item = opcao['nome']
            if custo:
                valor = getattr(custo, opcao['item'])
            else:
                valor = 0
            if valor is None:
                valor = 0
            else:
                valor = int(valor)            
            lista.append({'item':item, 'valor':valor})  
        context['lancado'] = lancado
        context['data'] = lista
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
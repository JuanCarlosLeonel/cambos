from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.models import Setor, Periodo, User
from produto.models import Producao, Desempenho, Custo, Perda, Material, Consumo, ValorCompra
from core.form import UserCreationForm
from django.db.models import Sum
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
    custo = Custo.objects.get(
        setor = id_setor,
        periodo = id_periodo
    )
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
        
        total_planejado = Desempenho.objects.get(
            setor = setor.id,
            periodo = periodo.id
        ).total_planejado

        try:
            eficiencia = (producao / total_planejado) * 100
        except:
            eficiencia = 0

        custo = custo_setor(setor.id, periodo.id)[1]
        try:
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
class DesempenhoList(ListView):
    model= Desempenho
    template_name = 'core/desempenho_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        lista = []
        opcoes= [
            'capacidade_total',
            'dias_trabalhados',
            'total_planejado',
            'headcount',
            'expedidores',
            'revisores',
            'setup',
            'carga_descarga',
            'manutencao_corretiva',
            'manutencao_preventiva',
            'total_alvejado',
            'total_chamuscado',
            'total_expedido',
            'total_recebido',
            'total_tingido',
        ]
    
        if setor.id < 5:            
            unidade_prod = 'kg'
        else:            
            unidade_prod = 'm'
       
        desempenho = Desempenho.objects.get(
            periodo = periodo.id,
            setor = setor.id
        )
        for opcao in opcoes:
            lista.append({'item':opcao, 'valor':getattr(desempenho, opcao), 'un':'seila'})
       
                
                
        context['data'] = lista
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
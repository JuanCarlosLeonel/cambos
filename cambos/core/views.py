from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.models import Setor, Periodo
from produto.models import Producao, Desempenho, Custo, Perda, Material, Consumo, ValorCompra
from django.db.models import Sum

def custo_setor(id_setor, id_periodo):
    custo = Custo.objects.get(
        setor = id_setor,
        periodo = id_periodo
    )
    custo_total = custo.energia + custo.laboratorio + custo.manutencao + custo.material_uso_continuo + custo.mao_de_obra + custo.vapor + custo.agua
    return custo_total

def compra_setor(id_setor, id_periodo):
    lista = []
    consumo = Consumo.objects.filter(
        setor = id_setor,
        periodo = id_periodo,
        material__origem = "Compra",
        material__tipo = "Insumo"
    )
    total_geral = 0
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
        total_geral += preco * item.quantidade

    return lista,total_geral


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.request.GET.get('periodo', None)
        if not periodo:
            periodo = "Agosto/2020"

        context['periodo'] = periodo
        return context



@method_decorator(login_required, name='dispatch')
class TextilP(TemplateView):
    template_name = 'core/textilp.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ultimo_periodo = Periodo.objects.latest('periodo')
        try:
            get_periodo = self.request.GET.get('periodo', None)
            periodo = Periodo.objects.get(nome = get_periodo)
        except:                    
            periodo = ultimo_periodo
        setor = Setor.objects.get(id = self.kwargs['pk'])        
        producao = Producao.objects.filter(
            setor = setor.id,
            periodo = periodo.id
        ).aggregate(Sum('quantidade'))['quantidade__sum']
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
        custo = custo_setor(setor.id, periodo.id)
        perda = Perda.objects.filter(
            setor = setor.id,
            periodo = periodo.id
        ).aggregate(Sum('quantidade'))['quantidade__sum']
        consumo = Consumo.objects.filter(
            setor = setor.id,
            periodo = periodo.id
        )
        try:
            perda_un = (perda / producao) * 100
        except:
            perda_un = 0
        insumo = compra_setor(setor.id, periodo.id)[1]
        
        try:
            insumo_un = insumo / producao
        except:
            insumo_un = 0
        material_consumido = consumo.filter(
            material__tipo = "Material",   
            periodo = periodo.id         
        )                
        valor_consumo_material = 0
        for item in material_consumido:
            if item.material.origem == "Compra":
                try:
                    preco = ValorCompra.objects.get(material__id = item.material.id, periodo = periodo.id).valor
                except:
                    preco = ValorCompra.objects.filter(material__id = item.material.id).latest('periodo').valor
                valor_consumo_material += preco * item.quantidade
        try:
            materia_prim_un = valor_consumo_material / producao
        except:
            materia_prim_un = 0
        materia_prima = materia_prim_un
        context['materia_prima'] = materia_prima
        context['insumo'] = insumo_un
        context['perda'] = perda_un
        context['custo'] = custo / producao
        context['eficiencia'] = (producao / total_planejado)*100
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = producao
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
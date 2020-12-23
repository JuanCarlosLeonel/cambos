from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.models import Setor, Periodo
from produto.models import Producao, Desempenho, Custo, Perda, Material, Consumo
from django.db.models import Sum

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
        custo = Custo.objects.get(
            setor = setor.id,
            periodo = periodo.id
        )
        perda = Perda.objects.get(
            setor = setor.id,
            periodo = periodo.id
        ).quantidade
        consumo = Consumo.objects.filter(
            setor = setor.id,
            periodo = periodo.id
        )
        insumo = consumo.filter(
            material__tipo = "Insumo"
        ).aggregate(Sum('quantidade'))['quantidade__sum']
        context['insumo'] = insumo / producao
        context['perda'] = (perda / producao) * 100
        context['custo'] = (custo.energia + custo.laboratorio + custo.manutencao + custo.material_uso_continuo + custo.mao_de_obra + custo.vapor + custo.agua) / producao
        context['eficiencia'] = (producao / total_planejado)*100
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = producao
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
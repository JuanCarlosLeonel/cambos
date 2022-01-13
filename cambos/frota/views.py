from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Abastecimento, Manutencao, VeiculoAbastecimento, Viagem, Veiculo
from .form import ManutencaoForm, ViagemForm, AbastecimentoForm
from django.http import JsonResponse
from django.db.models import Sum
import datetime

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'frota/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context


@method_decorator(login_required, name='dispatch')
class VeiculoIndex(TemplateView):
    template_name = 'frota/veiculo_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        pk = self.kwargs['pk']
        veiculo = Veiculo.objects.get(id = pk)
        context['veiculo'] = veiculo
        return context


@method_decorator(login_required, name='dispatch')
class ViagemCreate(CreateView):
    model = Viagem
    form_class = ViagemForm

    def get_success_url(self):                
        return f'/frota/viagem_list/{self.kwargs["pk"]}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        context['veiculo'] = self.kwargs['pk']
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(ViagemCreate, self).get_initial(**kwargs)
        veiculo = Veiculo.objects.get(pk = self.kwargs['pk'])
        km = Viagem.objects.filter(veiculo = veiculo).latest("km_final").km_final
        initial['veiculo'] = veiculo
        initial['data_inicial'] = datetime.date.today()
        initial['hora_inicial'] = datetime.datetime.now()
        initial['km_inicial'] = km
        
        return initial


@method_decorator(login_required, name='dispatch')
class AbastecimentoCreate(CreateView):
    model = Abastecimento
    form_class = AbastecimentoForm

    def get_success_url(self):        
        return '/frota/abastecimento_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(AbastecimentoCreate, self).get_initial(**kwargs)
        initial['data'] = datetime.date.today()
        return initial


@method_decorator(login_required, name='dispatch')
class ViagemUpdate(UpdateView):
    model = Viagem
    form_class = ViagemForm
    
    def get_success_url(self):        
        return f'/frota/viagem_list/{self.object.veiculo.id}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        context['veiculo'] = self.object.veiculo.id
        return context


@method_decorator(login_required, name='dispatch')
class ViagemDelete(DeleteView):
    model = Viagem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context   

    def get_success_url(self):
        return f'/frota/viagem_list/{self.object.veiculo.id}'


@method_decorator(login_required, name='dispatch')
class AbastecimentoList(ListView):
    model = Abastecimento
    template_name = 'frota/abastecimento_list.html'


@method_decorator(login_required, name='dispatch')
class AbastecimentoUpdate(UpdateView):
    model = Abastecimento
    form_class = AbastecimentoForm
    
    def get_success_url(self):        
        return '/frota/abastecimento_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context


@method_decorator(login_required, name='dispatch')
class AbastecimentoDelete(DeleteView):
    model = Abastecimento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context   

    def get_success_url(self):
        return '/frota/abastecimento_list'


@method_decorator(login_required, name='dispatch')
class VeiculoList(ListView):
    model = Veiculo
    template_name = 'frota/veiculo_list.html'


@method_decorator(login_required, name='dispatch')
class ViagemList(ListView):
    model = Viagem
    template_name = 'frota/viagem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        pk = self.kwargs['pk']     
        lista_viagem = Viagem.objects.filter(veiculo = pk).order_by("-id")
        veiculo = Veiculo.objects.get(id = pk)
        context['veiculo']=veiculo
        context['lista']=lista_viagem
        return context  


@method_decorator(login_required, name='dispatch')
class ViagemListALL(ListView):
    model = Viagem
    template_name = 'frota/viagem_listALL.html'


def relatorio_despesa(request):
    from datetime import datetime
    x = Abastecimento.objects.all()
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    mes = datetime.now().month + 1
    ano = datetime.now().year
    for i in range(12): 
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        y = sum([i.valor_unitario for i in x if i.data.month == mes and i.data.year == ano])
        labels.append(meses[mes-1])
        data.append(y)
    data_json = {'data': data[::-1], 'labels': labels[::-1]}
    return JsonResponse(data_json)

def relatorio_abastecimento_porveiculo(request):
    produtos = VeiculoAbastecimento.objects.all()
    label = []
    data = []
    for produto in produtos:
        vendas = Abastecimento.objects.filter(veiculo=produto).aggregate(Sum('valor_unitario'))
        if not vendas['valor_unitario__sum']:
            vendas['valor_unitario__sum'] = 0
        label.append(produto.veiculo.descricao.descricao)
        data.append(vendas['valor_unitario__sum'])

    x = list(zip(label, data))
    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    
    return JsonResponse({'labels': x[0][:7], 'data': x[1][:7]})


def relatorio_manutencao_porveiculo(request):
    produtos = Veiculo.objects.all()
    label = []
    data = []
    for produto in produtos:
        valor = Manutencao.objects.filter(veiculo=produto).aggregate(Sum('valor'))
        if not valor['valor__sum']:
            valor['valor__sum'] = 0
        label.append(produto.descricao.descricao)
        data.append(valor['valor__sum'])

    x = list(zip(label, data))
    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    
    return JsonResponse({'labels': x[0][:7], 'data': x[1][:7]})


@method_decorator(login_required, name='dispatch')
class IndexDespesas(TemplateView):
    template_name = 'frota/despesas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context


@method_decorator(login_required, name='dispatch')
class ManutencaoList(ListView):
    model = Manutencao
    template_name = 'frota/manutencao_list.html'


@method_decorator(login_required, name='dispatch')
class ManutencaoCreate(CreateView):
    model = Manutencao
    form_class = ManutencaoForm

    def get_success_url(self):        
        return '/frota/manutencao_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(ManutencaoCreate, self).get_initial(**kwargs)
        return initial

@method_decorator(login_required, name='dispatch')
class ManutencaoUpdate(UpdateView):
    model = Manutencao
    form_class = ManutencaoForm
    
    def get_success_url(self):        
        return '/frota/manutencao_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context

@method_decorator(login_required, name='dispatch')
class ManutencaoDelete(DeleteView):
    model = Manutencao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context   

    def get_success_url(self):
        return '/frota/manutencao_list'
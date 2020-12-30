from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import (
    Producao,
    Material,
)
from core.models import (
    Setor,
    Periodo,
)
from .form import (
    ProducaoModalForm,
)

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


class ProducaoModalCreate(CreateView):
    model = Producao
    form_class = ProducaoModalForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        material = Material.objects.get(id = self.kwargs['pk'])
        periodo = get_periodo(self)
        setor = get_setor(self)        
        context['item'] = material.nome
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(ProducaoModalCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)
        material = Material.objects.get(id = self.kwargs['pk'])
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo
        initial['material'] = material
        return initial


class ProducaoModalUpdate(UpdateView):
    model = Producao
    form_class = ProducaoModalForm
    
    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material.nome
        context['item'] = item
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


class ProducaoDelete(DeleteView):
    model = Producao 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material.nome
        context['item'] = item
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context   

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'
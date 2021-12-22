from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Abastecimento, Viagem, Corrida
from .form import ViagemForm, AbastecimentoForm, CorridaForm

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'frota/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context


@method_decorator(login_required, name='dispatch')
class ViagemList(ListView):
    model = Viagem
    template_name = 'frota/viagem_list.html'


@method_decorator(login_required, name='dispatch')
class ViagemCreate(CreateView):
    model = Viagem
    form_class = ViagemForm

    def get_success_url(self):        
        return '/frota/viagem_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(ViagemCreate, self).get_initial(**kwargs)
        initial['data'] = '12/01/2022'
        
        return initial


@method_decorator(login_required, name='dispatch')
class CorridaList(ListView):
    model = Corrida
    template_name = 'frota/Corrida_list.html'


@method_decorator(login_required, name='dispatch')
class CorridaCreate(CreateView):
    model = Corrida
    form_class = CorridaForm

    def get_success_url(self):        
        return '/frota/corrida_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(CorridaCreate, self).get_initial(**kwargs)
        initial['data'] = '12/01/2022'
        
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
        initial['data'] = '12/01/2022'
        return initial


@method_decorator(login_required, name='dispatch')
class ViagemUpdate(UpdateView):
    model = Viagem
    form_class = ViagemForm
    
    def get_success_url(self):        
        return '/frota/viagem_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context


@method_decorator(login_required, name='dispatch')
class ViagemDelete(DeleteView):
    model = Viagem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context   

    def get_success_url(self):
        return '/frota/viagem_list'


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

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Abastecimento, Viagem, Veiculo
from .form import ViagemForm, AbastecimentoForm
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
        initial['data'] = '12/01/2022'
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
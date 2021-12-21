from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Viagem
from .form import ViagemForm

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'frota/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        return context


@method_decorator(login_required, name='dispatch')
class ViagemList(ListView):
    model = Viagem
    template_name = 'core/viagem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


@method_decorator(login_required, name='dispatch')
class ViagemCreate(CreateView):
    model = Viagem
    form_class = ViagemForm

    def get_success_url(self):        
        return '/core/viagem_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        
        return context
        
    
    def get_initial(self, *args, **kwargs):
        initial = super(ViagemCreate, self).get_initial(**kwargs)
        
        return initial
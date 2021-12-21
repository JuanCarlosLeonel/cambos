from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Viagem

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
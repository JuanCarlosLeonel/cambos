from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from roupa.models import FichaCorte

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):    
    template_name = 'qualidade/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
           
        return context


@method_decorator(login_required, name='dispatch')
class QualidadeDetail(TemplateView):    
    template_name = 'qualidade/qualidade_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs['pk']
        context['pedido'] = FichaCorte.objects.get(lacre = pk)
        return context

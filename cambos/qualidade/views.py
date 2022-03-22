from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from .models import PlanoDeAcao, Acao, QualidadeTrack, QualidadeBot
from .form import PlanoAcaoForm, AcaoForm
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
        context['planos_acao'] = PlanoDeAcao.objects.filter(referencia = pk)
        return context


@method_decorator(login_required, name='dispatch')
class PlanoAcaoCreate(CreateView):    
    model = PlanoDeAcao
    template_name = 'qualidade/plano_acao_form.html'
    form_class = PlanoAcaoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs['pk']
        context['pedido'] = FichaCorte.objects.get(lacre = pk)
        return context

    def get_success_url(self):
        pk = self.object.id
        return f'/qualidade/plano_acao_detail/{pk}'

    def get_initial(self, *args, **kwargs):
        initial = super(PlanoAcaoCreate, self).get_initial(**kwargs)
        lacre = self.kwargs['pk']
        initial['referencia'] = lacre
        return initial


@method_decorator(login_required, name='dispatch')
class PlanoAcaoDetail(TemplateView):    
    template_name = 'qualidade/plano_acao_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs['pk']
        plano = PlanoDeAcao.objects.get(id = pk)     
        try:
            ficha = FichaCorte.objects.get(lacre = plano.referencia).dados
        except:
            ficha = 'Não encontrada'
        context['plano'] = plano
        context['pedido'] = ficha
        context['acoes'] = Acao.objects.filter(plano_acao__id = pk)
        return context


@method_decorator(login_required, name='dispatch')
class AcaoCreate(CreateView):    
    model = Acao
    template_name = 'qualidade/acao_form.html'
    form_class = AcaoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs['pk']
        context['plano'] = PlanoDeAcao.objects.get(id = pk)
        return context

    def get_form_kwargs(self):
        usuario_list = QualidadeBot.objects.filter().values('usuario__id')
        kwargs = super().get_form_kwargs()
        kwargs['usuario_list'] = usuario_list
        return kwargs

    def get_success_url(self):            
        model = QualidadeTrack.objects.latest('pcp')    
        user = self.object.responsavel
        userbot = QualidadeBot.objects.get(usuario = user)
        ref = self.object.plano_acao.referencia
        model.pcp.append(
            {"lacre":ref,
            "tipo":"acao",
            "responsavel":userbot.user_id,
            "descricao":self.object.descricao,
            "ref":self.object.plano_acao.id
            }
        )
        model.save()
        pk = self.object.plano_acao
        return f'/qualidade/plano_acao_detail/{pk.id}'

    def get_initial(self, *args, **kwargs):
        initial = super(AcaoCreate, self).get_initial(**kwargs)
        plano = self.kwargs['pk']
        initial['plano_acao'] = PlanoDeAcao.objects.get(id = plano)
        return initial


@method_decorator(login_required, name='dispatch')
class AcaoUpdate(UpdateView):    
    model = Acao
    template_name = 'qualidade/acao_form.html'
    form_class = AcaoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs['pk']        
        context['plano'] = PlanoDeAcao.objects.get(id = self.object.plano_acao.id)
        return context

    def get_form_kwargs(self):
        usuario_list = QualidadeBot.objects.filter().values('usuario__id')
        kwargs = super().get_form_kwargs()
        kwargs['usuario_list'] = usuario_list
        return kwargs

    def get_success_url(self):
        pk = self.object.plano_acao
        return f'/qualidade/plano_acao_detail/{pk.id}'

    
@method_decorator(login_required, name='dispatch')
class AcaoList(TemplateView):    
    template_name = 'qualidade/acao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        context['acoes'] = Acao.objects.filter(data_fim__isnull = True)
        return context
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from core.models import Enderecos, SolicitacaoViagem, UserCompras
from .models import Abastecimento, ItemViagem, Manutencao, Motorista, Viagem, Veiculo, FrotaPermissao
from .form import  ManutencaoForm, ViagemForm, AbastecimentoForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
import datetime
from .filters import SolicitacaoFilter, ViagemFilter, ViagemFilterCarro, AbastecimentoFilter, AbastecimentoFilterCaminhao
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import telegram
from django.db.models.signals import post_save
from django import template

def enviar(sender, instance, created, **kwargs):
    if created:
        from roupa.models import RoupaBot
        from core.models import Bot
        bot = Bot.objects.latest('token')
        token = bot.token 
        users = RoupaBot.objects.filter(ativo = True)
        v = Viagem.objects.filter().latest('id')
        if v.veiculo.caminhao:
            for user in users:      
                if user.frota:  
                    chat_id = user.user_id
                    html_content = render_to_string('frota/telegram_message.html', {'nome': Viagem.objects.filter(veiculo__caminhao = True).latest('id')})
                    bot = telegram.Bot(token=token)
                    bot.send_message(chat_id=chat_id,text=html_content, parse_mode=telegram.ParseMode.HTML)
post_save.connect(enviar, sender=Viagem)

def enviarabastecimento(sender, instance, created, **kwargs):
    if created:
        from roupa.models import RoupaBot
        from core.models import Bot
        bot = Bot.objects.latest('token')
        token = bot.token 
        users = RoupaBot.objects.filter(ativo = True)
        for user in users:      
            if user.frota:  
                chat_id = user.user_id
        html_content = render_to_string('frota/telegram_messageabast.html', {'nome': Abastecimento.objects.latest('id')})
        bot = telegram.Bot(token=token)
        bot.send_message(chat_id=chat_id,text=html_content, parse_mode=telegram.ParseMode.HTML)
post_save.connect(enviarabastecimento, sender=Abastecimento)


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'frota/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        try:
            user_permission = FrotaPermissao.objects.get(usuario = self.request.user)
        except:
            user_permission = {}
        context['permissoes'] = user_permission
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
        context['nomeveiculo'] = Veiculo.objects.get(pk = self.kwargs['pk'])     
        context['veiculo'] = self.kwargs['pk']
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(ViagemCreate, self).get_initial(**kwargs)
        veiculo = Veiculo.objects.get(pk = self.kwargs['pk'])
        try:
            km= Viagem.objects.filter(veiculo = veiculo).exclude(km_final = None).latest("km_final").km_final
        except:
            km = None
        initial['veiculo'] = veiculo
        initial['data_inicial'] = datetime.date.today()
        initial['hora_inicial'] = datetime.datetime.now()
        initial['km_inicial'] = km
        return initial

    def get_form_kwargs(self):
        veiculo = Veiculo.objects.get(id = self.kwargs['pk'])
        if veiculo.caminhao:
            motoristas = Motorista.objects.filter().values('nome')
        else:
            motoristas = False
        kwargs = super().get_form_kwargs()
        kwargs['list_motorista'] = motoristas
        return kwargs


@method_decorator(login_required, name='dispatch')
class AbastecimentoCreate(CreateView):
    model = Abastecimento
    form_class = AbastecimentoForm

    def get_success_url(self):        
        return f'/frota/abastecimento_list/{self.kwargs["pk"]}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['nomeveiculo'] = Veiculo.objects.get(pk = self.kwargs['pk'])              
        context['veiculo'] = self.kwargs['pk']
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(AbastecimentoCreate, self).get_initial(**kwargs)
        veiculo = Veiculo.objects.get(pk = self.kwargs['pk'])
        initial['veiculo'] = veiculo
        if veiculo.caminhao:
            initial['combustivel'] = 'Diesel'
        else:
            initial['combustivel'] = 'Álcool','Gasolina'
        initial['data'] = datetime.date.today()
        return initial

    def get_form_kwargs(self):        
        veiculo = Veiculo.objects.get(pk = self.kwargs['pk'])
        kwargs = super().get_form_kwargs()                
        kwargs['inter'] = veiculo.caminhao
        return kwargs



@method_decorator(login_required, name='dispatch')
class ViagemUpdate(UpdateView):
    model = Viagem
    form_class = ViagemForm
    
    def get_success_url(self): 
        from datetime import timedelta
        v = self.object.id
        km = self.object.km_final
        i = ItemViagem.objects.filter(viagem = v)
        s = SolicitacaoViagem.objects.all()
        if km:
            for item in i:
                if item.viagem.id == v:
                    for sol in s:
                        if sol.id == item.viagem_solicitacao.id:
                            sol.situacao = '3'
                            sol.data_finalizacao = datetime.datetime.now() - timedelta(hours = +3)
                            sol.save()          
        else:
            pass     
        return f'/frota/viagem_list/{self.object.veiculo.id}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        context['veiculo'] = self.object.veiculo.id
        return context

    def get_initial(self):
        initial = super(ViagemUpdate, self).get_initial()
        veiculo = self.object.veiculo.id
        km= Viagem.objects.filter(veiculo = veiculo).exclude(km_final = None).latest("km_final").km_final
        viagem_object = self.get_object()
        if viagem_object.km_inicial == None or viagem_object.data_final == None or viagem_object.km_final == None:
            initial['km_inicial'] = km 
        return initial

    def get_form_kwargs(self):
        veiculo = self.object.veiculo
        if veiculo.caminhao:
            motoristas = Motorista.objects.filter().values('nome__id')
        else:
            motoristas = False
        kwargs = super().get_form_kwargs()
        kwargs['list_motorista'] = motoristas
        return kwargs


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        pk = self.kwargs['pk']     
        lista_abastecimento = Abastecimento.objects.filter(veiculo = pk).order_by("-id")
        veiculo = Veiculo.objects.get(id = pk)
        context['veiculo']=veiculo
        context['lista']=lista_abastecimento
        return context  


@method_decorator(login_required, name='dispatch')
class AbastecimentoUpdate(UpdateView):
    model = Abastecimento
    form_class = AbastecimentoForm
    
    def get_success_url(self):        
        return f'/frota/abastecimento_list/{self.object.veiculo.id}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        context['veiculo'] = self.object.veiculo.id
        return context

@method_decorator(login_required, name='dispatch')
class AbastecimentoDelete(DeleteView):
    model = Abastecimento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context   

    def get_success_url(self):
        return f'/frota/abastecimento_list/{self.object.veiculo.id}'


@method_decorator(login_required, name='dispatch')
class VeiculoList(ListView):
    model = Veiculo
    template_name = 'frota/veiculo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        lista_viagem = Viagem.objects.all().order_by("-id")              
        try:
            user_permission = FrotaPermissao.objects.get(usuario = self.request.user)
        except:
            user_permission = {}
        context['dataatual'] = datetime.date.today()
        context['permissoes'] = user_permission
        context['lista_viagem'] = lista_viagem
        return context

@method_decorator(login_required, name='dispatch')
class SolicitacoesList(TemplateView):  
    template_name = 'frota/viagem_solicitacao_list.html'

    def get(self, request, *args, **kwargs):
        from datetime import timedelta
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk'] 

        endereco = Enderecos.objects.all()
        usercompras = UserCompras.objects.all()
        viag = Viagem.objects.get(id = pk)
        edit = self.request.GET.get('editar')
        value = self.request.GET.get('solicitacao_id')
        itemviagem = ItemViagem.objects.filter(viagem = viag)
        itemv = len(itemviagem)
        lista_solicitacoes = SolicitacaoViagem.objects.exclude(situacao = '3').order_by("-id")

        for solicitacao in lista_solicitacoes:
            for item in itemviagem:
                if item.viagem_solicitacao == solicitacao:
                    solicitacao.set_has_item(True)

        if edit == 'true':
            solicitacao = SolicitacaoViagem.objects.get(pk=value)
            solicitacao.situacao = '2'
            solicitacao.data_atendimento = datetime.datetime.now() - timedelta(hours = +3)
            solicitacao.save()
            model = ItemViagem(viagem = viag, viagem_solicitacao = solicitacao)
            model.save()
        elif edit == 'false':
            solicitacao = SolicitacaoViagem.objects.get(pk=value)
            solicitacao.situacao = '1'
            solicitacao.data_atendimento = None
            solicitacao.save()
            model = ItemViagem.objects.get(viagem = viag, viagem_solicitacao = solicitacao)
            model.delete()
        context['itemviagem'] = itemviagem
        context['itemv'] = itemv
        context['viag'] = viag
        context['user'] = usercompras
        context['endereco'] = endereco
        context['lista_solicitacoes']=lista_solicitacoes

        if not edit is None :  
            return redirect(f'/frota/viagem_solicitacao_list/{viag.id}')
        else:
            return render(request, 'frota/viagem_solicitacao_list.html', context)

@method_decorator(login_required, name='dispatch')
class ViagemList(ListView):
    model = Viagem
    template_name = 'frota/viagem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        pk = self.kwargs['pk']     
        veiculo = Veiculo.objects.get(id = pk)
        lista_viagem = Viagem.objects.filter(veiculo = pk).order_by("-id")
        context['dataatual'] = datetime.date.today()
        context['horaatual'] = datetime.datetime.now().time().strftime('%H:%M')
        context['veiculo']=veiculo
        context['lista']=lista_viagem
        return context


@method_decorator(login_required, name='dispatch')
class RelatorioList(ListView):
    model = Abastecimento
    template_name = 'frota/relatorio_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        return context


@method_decorator(login_required, name='dispatch')
class RelatorioViagemSolicitacao(ListView):
    model = SolicitacaoViagem
    template_name = 'frota/relatorio_viagemsolicitacao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        endereco = Enderecos.objects.all()
        usercompras = UserCompras.objects.all()
        itemviagem = ItemViagem.objects.all()
        lista = SolicitacaoFilter(self.request.GET, queryset=self.get_queryset())
        count = 0
        somakm = 0
        somahora = datetime.timedelta()
        subdata = datetime.timedelta()
        # for item in lista.qs:
        #     if item.veiculo.caminhao:
        #         count += 1
        #         if item.hora_final:
        #             inicial = datetime.timedelta(hours=item.hora_inicial.hour, minutes=item.hora_inicial.minute, seconds=item.hora_inicial.second)
        #             final = datetime.timedelta(hours=item.hora_final.hour, minutes=item.hora_final.minute, seconds=item.hora_final.second)
        #             diferencahoras = final -inicial
        #             somahora += diferencahoras
        #             if item.data_final > item.data_inicial and item.hora_inicial < item.hora_final:
        #                 subdata = item.data_final - item.data_inicial
        #             else:
        #                 pass
        #         else:
        #             pass
        #         if item.kmfinalmenosinicial:																					
        #             somakm += item.kmfinalmenosinicial
        # s = somahora + subdata
        # horas =  s.total_seconds() // 3600
        # minutos = s.total_seconds() % 3600/60
        # context['horas'] = horas
        # context['minutos'] = minutos
        context['itemviagem'] = itemviagem
        context['user'] = usercompras
        context['endereco'] = endereco
        context['somakm'] = somakm
        context['counter'] = count
        context['filter'] = lista
        return context  


@method_decorator(login_required, name='dispatch')
class RelatorioViagem(ListView):
    model = Viagem
    template_name = 'frota/relatorio_viagem.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = ViagemFilter(self.request.GET, queryset=self.get_queryset())
        count = 0
        somakm = 0
        somahora = datetime.timedelta()
        subdata = datetime.timedelta()
        for item in lista.qs:
            if item.veiculo.caminhao:
                count += 1
                if item.hora_final:
                    inicial = datetime.timedelta(hours=item.hora_inicial.hour, minutes=item.hora_inicial.minute, seconds=item.hora_inicial.second)
                    final = datetime.timedelta(hours=item.hora_final.hour, minutes=item.hora_final.minute, seconds=item.hora_final.second)
                    diferencahoras = final -inicial
                    somahora += diferencahoras
                    if item.data_final > item.data_inicial and item.hora_inicial < item.hora_final:
                        subdata = item.data_final - item.data_inicial
                    else:
                        pass
                else:
                    pass
                if item.kmfinalmenosinicial:																					
                    somakm += item.kmfinalmenosinicial
        s = somahora + subdata
        horas =  s.total_seconds() // 3600
        minutos = s.total_seconds() % 3600/60
        context['horas'] = horas
        context['minutos'] = minutos
        context['somakm'] = somakm
        context['counter'] = count
        context['filter'] = lista
        return context  


@method_decorator(login_required, name='dispatch')
class RelatorioViagemCarro(ListView):
    model = Viagem
    template_name = 'frota/relatorio_viagemcarro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista = ViagemFilterCarro(self.request.GET, queryset=self.get_queryset())
        count = 0
        somakm = 0
        somahora = datetime.timedelta()
        subdata = datetime.timedelta()
        for item in lista.qs:
            if not item.veiculo.caminhao :
                count += 1
                if item.hora_final:
                    inicial = datetime.timedelta(hours=item.hora_inicial.hour, minutes=item.hora_inicial.minute, seconds=item.hora_inicial.second)
                    final = datetime.timedelta(hours=item.hora_final.hour, minutes=item.hora_final.minute, seconds=item.hora_final.second)
                    diferencahoras = final -inicial
                    somahora += diferencahoras
                    if item.data_final > item.data_inicial and item.hora_inicial < item.hora_final:
                        subdata = item.data_final - item.data_inicial
                    else:
                        pass
                else:
                    pass
                if item.kmfinalmenosinicial:																					
                    somakm += item.kmfinalmenosinicial
        s = somahora + subdata
        s = somahora + subdata
        horas =  s.total_seconds() // 3600
        minutos = s.total_seconds() % 3600/60
        context['horas'] = horas
        context['minutos'] = minutos
        context['somakm'] = somakm
        context['counter'] = count
        context['filter'] = lista
        return context  


@method_decorator(login_required, name='dispatch')
class RelatorioAbastecimento(ListView):
    model = Abastecimento
    template_name = 'frota/relatorio_abastecimentocarro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        abastecimento = AbastecimentoFilter(self.request.GET, queryset=self.get_queryset())
        tot = 0
        valor = 0
        for item in abastecimento.qs:
            if not item.veiculo.caminhao:
                tot += item.quantidade
                valor += item.valor_unitario

        context['valor'] = valor
        context['tot'] = tot
        context['filter'] = abastecimento
        return context

@method_decorator(login_required, name='dispatch')
class RelatorioAbastecimentoCaminhao(ListView):
    model = Abastecimento
    template_name = 'frota/relatorio_abastecimentocaminhao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        abastecimento = AbastecimentoFilterCaminhao(self.request.GET, queryset=self.get_queryset())
        tot = 0
        valor = 0
        for item in abastecimento.qs:
            if item.veiculo.caminhao:
                tot += item.quantidade
                valor += item.valor_unitario

        context['valor'] = valor
        context['tot'] = tot
        context['filter'] = abastecimento
        return context

@method_decorator(login_required, name='dispatch')
class AbastecimentoListALL(ListView):
    model = Abastecimento
    template_name = 'frota/abastecimento_listALL.html'


def relatorio_despesa(request):
    from datetime import datetime
    x = Abastecimento.objects.filter(veiculo__caminhao = False)
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

def relatorio_despesacaminhao(request):
    from datetime import datetime
    x = Abastecimento.objects.filter(veiculo__caminhao = True)
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

def relatorio_abastecimento_porcaminhao(request):
    produtos = Veiculo.objects.filter(caminhao = True)
    label = []
    data = []
    for produto in produtos:
        vendas = Abastecimento.objects.filter(veiculo=produto).aggregate(Sum('valor_unitario'))
        if not vendas['valor_unitario__sum']:
            vendas['valor_unitario__sum'] = 0
        label.append(produto.descricao.descricao)
        data.append(vendas['valor_unitario__sum'])

    x = list(zip(label, data))
    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    
    return JsonResponse({'labels': x[0][:7], 'data': x[1][:7]})

def relatorio_abastecimento_porveiculo(request):
    produtos = Veiculo.objects.filter(caminhao = False)
    label = []
    data = []
    for produto in produtos:
        vendas = Abastecimento.objects.filter(veiculo=produto).aggregate(Sum('valor_unitario'))
        if not vendas['valor_unitario__sum']:
            vendas['valor_unitario__sum'] = 0
        label.append(produto.descricao.descricao)
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
        totabastecimentocarro = Abastecimento.objects.filter(veiculo__caminhao = False).aggregate(Sum('valor_unitario'))
        totabastecimentocaminhao = Abastecimento.objects.filter(veiculo__caminhao = True).aggregate(Sum('valor_unitario'))
        totmanutencao = Manutencao.objects.aggregate(Sum('valor'))
        context['totabastecimentocarro']=totabastecimentocarro
        context['totabastecimentocaminhao']=totabastecimentocaminhao
        context['totmanutencao']=totmanutencao       
        return context


@method_decorator(login_required, name='dispatch')
class ManutencaoListALL(ListView):
    model = Manutencao
    template_name = 'frota/manutencao_listALL.html'



@method_decorator(login_required, name='dispatch')
class ManutencaoList(ListView):
    model = Manutencao
    template_name = 'frota/manutencao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        pk = self.kwargs['pk']     
        lista_manutencao = Manutencao.objects.filter(veiculo = pk).order_by("-id")
        veiculo = Veiculo.objects.get(id = pk)
        context['veiculo']=veiculo
        context['lista']=lista_manutencao
        return context  


@method_decorator(login_required, name='dispatch')
class ManutencaoCreate(CreateView):
    model = Manutencao
    form_class = ManutencaoForm

    def get_success_url(self):        
        return f'/frota/manutencao_list/{self.kwargs["pk"]}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['nomeveiculo'] = Veiculo.objects.get(pk = self.kwargs['pk'])              
        context['veiculo'] = self.kwargs['pk']
        return context        
    
    def get_initial(self, *args, **kwargs):
        initial = super(ManutencaoCreate, self).get_initial(**kwargs)
        veiculo = Veiculo.objects.get(pk = self.kwargs['pk'])
        initial['veiculo'] = veiculo
        initial['data'] = datetime.date.today()
        return initial
    


@method_decorator(login_required, name='dispatch')
class ManutencaoUpdate(UpdateView):
    model = Manutencao
    form_class = ManutencaoForm
    
    def get_success_url(self):        
        return f'/frota/manutencao_list/{self.object.veiculo.id}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        context['veiculo'] = self.object.veiculo.id
        return context

@method_decorator(login_required, name='dispatch')
class ManutencaoDelete(DeleteView):
    model = Manutencao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context   

    def get_success_url(self):
        return f'/frota/viagem_list/{self.object.veiculo.id}'
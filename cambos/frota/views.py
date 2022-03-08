from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from .models import Abastecimento, Manutencao, Motorista, Viagem, Veiculo, FrotaPermissao
from .form import ManutencaoForm, ViagemForm, AbastecimentoForm
from django.http import JsonResponse
from django.db.models import Sum
import datetime
from .filters import ViagemFilter, ViagemFilterCarro, AbastecimentoFilter, AbastecimentoFilterCaminhao

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
        context['permissoes'] = user_permission
        context['lista_viagem'] = lista_viagem
        return context

@method_decorator(login_required, name='dispatch')
class ViagemList(ListView):
    model = Viagem
    template_name = 'frota/viagem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        pk = self.kwargs['pk']     
        lista_viagem = Viagem.objects.filter(veiculo = pk).order_by("-id")
        try:
            ultima = Viagem.objects.filter(veiculo=pk).latest('id')
            context['ultima']=ultima
        except:
            pass
        veiculo = Veiculo.objects.get(id = pk)
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
        if (len(f"{str(s)[0:2]}dias,{str(s)[7:]}")) >= 10:
            context['somahora'] = (f"{str(s)[0:2]}dias{str(s)[7:]}")
        else :
            context['somahora'] = s
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
        if (len(f"{str(s)[0:2]}dias,{str(s)[7:]}")) >= 10:
            context['somahora'] = (f"{str(s)[0:2]}dias {str(s)[7:]}")
        else :
            context['somahora'] = s
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
    produtos = Veiculo.objects.all()
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
        totabastecimento = Abastecimento.objects.aggregate(Sum('valor_unitario'))
        totmanutencao = Manutencao.objects.aggregate(Sum('valor'))
        context['totabastecimento']=totabastecimento
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
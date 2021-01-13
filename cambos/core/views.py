from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Setor, Periodo, User
from produto.models import (
    Producao,
    Desempenho,
    Custo,
    Perda,
    Material,
    Consumo,
    ValorCompra,
    Custo
)
from .form import UserCreationForm
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy


class UserCreate(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy('core_index')


def get_periodo(self):
    try:
        periodo = Periodo.objects.get(nome=self.request.GET.get('periodo', None))
    except:
        periodo = Periodo.objects.latest('periodo')
    return periodo


def get_setor(self):
    try:
        setor = Setor.objects.get(id=self.request.GET.get('setor', None))
    except:
        setor = 0
    return setor


def producao_setor(setor, id_periodo):
    if setor == 0:
        producao = Producao.objects.filter(
            setor__nome="Revisão",
            periodo=id_periodo
        )
    else:
        producao = Producao.objects.filter(
            setor=setor,
            periodo=id_periodo
        )
    total = producao.aggregate(Sum('quantidade'))['quantidade__sum']
    return {'producao':producao, 'total':total}


def perda_setor(setor, id_periodo):
    if setor == 0:
        perda = Perda.objects.filter(
            periodo=id_periodo
        )
    else:
        perda = Perda.objects.filter(
            setor=setor,
            periodo=id_periodo
        )
    total = perda.aggregate(Sum('quantidade'))['quantidade__sum']
    return {'perda':perda,'total':total}


def custo_setor(setor, id_periodo):
    if setor == 0:
        custo_total = 0
        custo_lista = Custo.objects.filter(periodo=id_periodo)
        for custo in custo_lista:
            custo_total += custo.energia + custo.laboratorio + custo.manutencao + custo.material_uso_continuo + custo.mao_de_obra + custo.vapor + custo.agua
    else:
        try:
            custo = Custo.objects.get(
                periodo=id_periodo,
                setor=setor
            )
        except:
            custo = Custo.objects.filter(setor=setor).latest('periodo')
        custo_total = custo.energia + custo.laboratorio + custo.manutencao + custo.material_uso_continuo + custo.mao_de_obra + custo.vapor + custo.agua
    return {'custo_total': custo_total}


def compra_setor(setor, id_periodo):
    lista = []
    if setor == 0:
        consumo = Consumo.objects.filter(
            periodo=id_periodo,
            material__origem="Compra",
        )
    else:
        consumo = Consumo.objects.filter(
            setor=setor,
            periodo=id_periodo,
            material__origem="Compra",
        )
    total_insumo = 0
    total_material = 0
    for item in consumo:
        try:
            preco = ValorCompra.objects.get(material__id=item.material.id, periodo=id_periodo).valor
        except:
            try:
                preco = ValorCompra.objects.filter(material__id=item.material.id).latest('periodo').valor
            except:
                preco = 0
        lista.append({
            'tipo': item.material.tipo,
            'material': item.material,
            'quantidade': item.quantidade,
            'valor': preco,
            'total': preco * item.quantidade
        })
        if item.material.tipo == "Insumo":
            total_insumo += preco * item.quantidade
        elif item.material.tipo == "Material":
            total_material += preco * item.quantidade

    return {'lista': lista, 'total_insumo': total_insumo, 'total_material': total_material}


def preco_material(id_material, periodo):
    preco = 0
    material = Material.objects.get(
        id=id_material
    )
    if material.origem == "Compra":
        historico_compra = ValorCompra.objects.filter(material=material).aggregate(
            Count('id'))['id__count']
        if historico_compra == 0:
            preco = 0
        else:
            try:
                preco = ValorCompra.objects.get(
                    material=material,
                    periodo=periodo
                ).valor
            except:
                ultima_compra = ValorCompra.objects.filter(material=material).latest('periodo').valor
                preco = ultima_compra
    else:
        setor_origem = Setor.objects.get(nome=material.origem)
        custo_setor_origem = custo_setor(setor_origem, periodo)['custo_total']
        compra_setor_origem = compra_setor(setor_origem, periodo)

        producao = producao_setor(setor_origem, periodo)['total']
        if producao is None:
            producao = Producao.objects.filter(setor=setor_origem, periodo=(periodo.id - 1)).aggregate(
                Sum('quantidade'))['quantidade__sum']
        produto_interno = Consumo.objects.filter(
            periodo=periodo,
            setor=setor_origem,
        ).exclude(material__origem="Compra")
        preco2 = 0
        for item in produto_interno:
            setor_origem2 = Setor.objects.get(nome=item.material.origem)
            custo_setor_origem2 = custo_setor(setor_origem2, periodo)['custo_total']
            compra_setor_origem2 = compra_setor(setor_origem2, periodo)
            producao2 = producao_setor(setor_origem, periodo)['total']
            preco2 = (custo_setor_origem2 + compra_setor_origem2['total_insumo'] + compra_setor_origem2[
                'total_material']) / producao2

        try:
            preco = ((custo_setor_origem + compra_setor_origem['total_insumo'] + compra_setor_origem[
                'total_material']) / producao) + preco2
        except:
            preco = 0

    return preco


def preco_material_periodo(setor, id_periodo):
    total = 0
    if setor == 0:
        lista_consumo = Consumo.objects.filter(
            periodo=id_periodo,
            material__tipo="Material",
            material__origem="Compra"
        )
    else:
        lista_consumo = Consumo.objects.filter(
            setor=setor,
            periodo=id_periodo,
            material__tipo="Material"
        )
    for item in lista_consumo:
        preco = preco_material(item.material.id, id_periodo)
        quantidade = item.quantidade
        valor = preco * quantidade

        total += valor
    return total


def dash(nome_periodo, id_periodo, setor):
    meses_abr = ["Jan", "fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    periodo_ind = meses_abr.index(nome_periodo[0:3])
    if periodo_ind == 11:
        p_inicio = 0
    else:
        p_inicio = periodo_ind + 1
    p_fim = 0
    id_periodo -= 11
    label_periodo = []
    prod_periodo = []
    insumo_periodo = []
    material_periodo = []
    custo_periodo = []        
    while (p_fim < 12):
        p_fim += 1
        label_periodo.append(meses_abr[p_inicio])
        producao = producao_setor(setor, id_periodo)['total']
        if not producao:
            producao = 0
        try:
            insumo = compra_setor(setor, id_periodo)['total_insumo'] / producao
        except:
            insumo = 0
        try:
            custo = custo_setor(setor, id_periodo)['custo_total'] / producao
        except:
            custo = 0
        try:
            material = preco_material_periodo(setor, id_periodo) / producao
        except:
            material = 0
        prod_periodo.append(int(producao))
        insumo_periodo.append(round(insumo, 2))
        material_periodo.append(round(material, 2))
        custo_periodo.append(round(custo, 2))        
        id_periodo += 1
        if p_inicio == 11:
            p_inicio = 0
        else:
            p_inicio += 1
    return {
        'label': label_periodo,        
        'producao': prod_periodo,
        'insumo': insumo_periodo,
        'material': material_periodo,
        'custo': custo_periodo
    }


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        producao = producao_setor(setor, periodo)['total']
        if not setor or setor == 0:
            unidades = 'Metros'
            unidade = 'Metro'
        elif setor.id < 3:
            unidades = 'Quilos'
            unidade = 'Quilo'
        else:
            unidades = 'Metros'
            unidade = 'Metro'
        try:
            if setor == 0:
                total_planejado = Desempenho.objects.get(
                    setor__nome="Revisão",
                    periodo=periodo.id
                ).total_planejado
            else:
                total_planejado = Desempenho.objects.get(
                    setor=setor,
                    periodo=periodo.id
                ).total_planejado
        except:
            total_planejado = 0
        try:
            eficiencia = (producao / total_planejado) * 100
        except:
            eficiencia = 0

        custo = custo_setor(setor, periodo)['custo_total']
        try:
            custo_un = custo / producao
        except:
            custo_un = 0

        perda = perda_setor(setor, periodo)['total']
        try:
            perda_un = (perda / producao) * 100
        except:
            perda_un = 0

        insumo = compra_setor(setor, periodo)['total_insumo']
        try:
            insumo_un = insumo / producao
        except:
            insumo_un = 0

        valor_consumo_material = preco_material_periodo(setor, periodo)
        try:
            materia_prim_un = valor_consumo_material / producao
        except:
            materia_prim_un = 0

        dashboard = dash(periodo.nome, periodo.id, setor)
        if setor == 0:
            setor = {'nome': 'Consolidado'}

        context['data1'] = dashboard['producao']
        context['data2'] = dashboard['custo']
        context['data3'] = dashboard['insumo']
        context['data4'] = dashboard['material']
        context['labels1'] = dashboard['label']        
        context['materia_prima'] = materia_prim_un
        context['insumo'] = insumo_un
        context['perda'] = perda_un
        context['custo'] = custo_un
        context['eficiencia'] = eficiencia
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = producao
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class ProducaoList(TemplateView):    
    template_name = 'core/producao_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        get_producao = producao_setor(setor, periodo.id)
        producao = get_producao['producao']
        total = get_producao['total']

        if not total:
            total = 0
        lista = []        
        if setor == 0:
            origem = "Tecelagem"
        elif setor.id < 5:
            origem = setor.nome
        else:
            origem = "Tecelagem"

        historico = Producao.objects.filter(
            Q(material__origem=origem,),                
            Q(periodo__id= periodo.id - 1) |
            Q(periodo__id= periodo.id)                        
        ).distinct('material')

        for material in historico:
            material_nome = material.material.nome
            material_unidade = material.material.unidade
            quantidade = 0
            percentual = 0
            id_producao = ''
            id_material = material.material.id
            for item in producao:
                if item.material.id == material.material.id:
                    quantidade = item.quantidade
                    percentual = (item.quantidade / total) * 100
                    id_producao = item.id
            if material.material.inativo and quantidade == 0:
                pass
            else:
                lista.append({
                    'material': material_nome,
                    'material_unidade': material_unidade,
                    'quantidade': quantidade,
                    'percentual': percentual,
                    'id': id_producao,
                    'id_material': id_material
                })
        if setor == 0:
            setor = {
                'nome': 'Consolidado',
            }        
        context['producaojs'] = sorted(lista, key=lambda x: x['quantidade'], reverse=True)
        context['producao'] = total
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class PerdaList(ListView):
    model = Perda
    template_name = 'core/perda_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        perdas = perda_setor(setor, periodo)
        perda = perdas['perda']
        total = perdas['total']
        if setor.id < 5:
            unidades = 'Quilos'
            unidade = 'kg'
        else:
            unidades = 'Metros'
            unidade = 'm'
        lista = []
        historico = Perda.objects.filter(
            setor=setor,
        ).distinct('material')
        for material in historico:
            material_nome = material.material.nome
            quantidade = 0
            percentual = 0
            id_perda = ''
            id_material = material.material.id
            for item in perda.distinct('material'):
                if item.material.id == material.material.id:
                    quantidade = item.quantidade
                    try:
                        percentual = (item.quantidade / total) * 100
                    except:
                        percentual = 0
                    id_perda = item.id
            if material.material.inativo and quantidade == 0:
                pass
            else:
                lista.append({
                    'material': material_nome,
                    'quantidade': quantidade,
                    'percentual': percentual,
                    'id': id_perda,
                    'id_material': id_material
                })
        context['producaojs'] = sorted(lista, key=lambda x: x['quantidade'], reverse=True)
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = total
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class ConsumoMaterialList(ListView):
    model = Consumo
    template_name = 'core/consumo_material_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        lista = []            
        quantidade = 0
        preco = 0
        total = 0
        valor = 0
        if setor == 0:
            consumo = Consumo.objects.filter(
                periodo=periodo.id,
                material__tipo="Material",
                material__origem="Compra"
            )            

            for consumido in consumo:
                quantidade = consumido.quantidade
                preco = preco_material(consumido.material.id, periodo)
                valor = quantidade * preco
                total += valor

            for item in consumo:
                quantidade = 0
                percentual = 0
                valor = 0
                material_nome = item.material.nome
                material_unidade = item.material.unidade
                origem = item.material.origem                
                preco = preco_material(item.material.id, periodo)                                
                quantidade = item.quantidade
                valor = quantidade * preco
                try:
                    percentual = (valor / total) * 100
                except:
                    percentual = 0                
        
                lista.append({
                    'material': material_nome,
                    'material_unidade': material_unidade,
                    'origem': origem,
                    'quantidade': quantidade,
                    'preco': preco,
                    'percentual': percentual,
                    'valor': valor,                    
                    'setor': item.setor.nome
                })        
            setor = {
                'nome': 'Consolidado',
            }
        else:
            consumo = Consumo.objects.filter(
                setor=setor,
                periodo=periodo.id,
                material__tipo="Material"
            )
            historico = Consumo.objects.filter(
                Q(setor=setor),
                Q(material__tipo="Material"),
                Q(periodo__id= periodo.id - 1)|
                Q(periodo__id= periodo.id)
                
            ).distinct('material')        
        
            for consumido in consumo:
                quantidade = consumido.quantidade
                preco = preco_material(consumido.material.id, periodo)
                valor = quantidade * preco
                total += valor

            for item in historico:
                material_nome = item.material.nome
                material_unidade = item.material.unidade
                origem = item.material.origem
                quantidade = 0
                preco = preco_material(item.material.id, periodo)
                percentual = 0
                id_consumo = ''
                id_material = item.material.id
                valor = 0

                for consumido in consumo:
                    if consumido.material.id == item.material.id:
                        quantidade = consumido.quantidade
                        valor = quantidade * preco
                        try:
                            percentual = (valor / total) * 100
                        except:
                            percentual = 0
                        id_consumo = consumido.id
                if item.material.inativo and quantidade == 0:
                    pass
                else:
                    lista.append({
                        'material': material_nome,
                        'material_unidade': material_unidade,
                        'origem': origem,
                        'quantidade': quantidade,
                        'preco': preco,
                        'percentual': percentual,
                        'valor': valor,
                        'id': id_consumo,
                        'id_material': id_material,
                        'setor': item.setor.nome
                    })        
        context['total'] = total        
        context['producaojs'] = sorted(lista, key=lambda x: x['valor'], reverse=True)
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class ConsumoInsumoList(ListView):
    model = Consumo
    template_name = 'core/consumo_insumo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        lista = []            
        quantidade = 0
        preco = 0
        total = 0
        valor = 0
        if setor == 0:
            consumo = Consumo.objects.filter(                
                periodo=periodo,
                material__tipo="Insumo",
            )            
            for item in consumo:
                quantidade = item.quantidade
                preco = preco_material(item.material.id, periodo)
                valor = quantidade * preco
                total += valor

            for item in consumo:                
                percentual = 0                
                material_nome = item.material.nome                
                preco = preco_material(item.material.id, periodo)                                
                valor = 0
                quantidade = item.quantidade
                valor = quantidade * preco
                try:
                    percentual = (valor / total) * 100
                except:
                    percentual = 0                
                
                lista.append({
                    'material': material_nome,
                    'quantidade': quantidade,
                    'preco': preco,
                    'percentual': percentual,
                    'valor': valor,                    
                    'setor': item.setor.nome
                })
            setor = {
                'nome': 'Consolidado',
            }
        else:
            consumo = Consumo.objects.filter(
                setor=setor,
                periodo=periodo.id,
                material__tipo="Insumo",
            )

            historico = Consumo.objects.filter(
                Q(setor=setor),
                Q(material__tipo="Insumo"),
                Q(periodo__id= periodo.id - 1)|
                Q(periodo__id= periodo.id)
                
            ).distinct('material') 
        
            for consumido in consumo:
                quantidade = consumido.quantidade
                preco = preco_material(consumido.material.id, periodo)
                valor = quantidade * preco
                total += valor

            for item in historico:
                material_nome = item.material.nome
                quantidade = 0
                preco = preco_material(item.material.id, periodo)
                percentual = 0
                id_consumo = ''
                id_material = item.material.id
                valor = 0

                for consumido in consumo:
                    if consumido.material.id == item.material.id:
                        quantidade = consumido.quantidade
                        valor = quantidade * preco
                        try:
                            percentual = (valor / total) * 100
                        except:
                            percentual = 0
                        id_consumo = consumido.id
                if item.material.inativo and quantidade == 0:
                    pass
                else:
                    lista.append({
                        'material': material_nome,
                        'quantidade': quantidade,
                        'preco': preco,
                        'percentual': percentual,
                        'valor': valor,
                        'id': id_consumo,
                        'id_material': id_material,
                        'setor': item.setor.nome
                    })        
        context['total'] = total        
        context['producaojs'] = sorted(lista, key=lambda x: x['valor'], reverse=True)
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class DesempenhoList(ListView):
    model = Desempenho
    template_name = 'core/desempenho_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        if setor.id < 5:
            unidade_prod = 'kilos'
        else:
            unidade_prod = 'metros'
        lista = []
        opcoes = [
            {'item': 'capacidade_total',
             'nome': 'Capacidade Total',
             'un': unidade_prod},
            {'item': 'dias_trabalhados',
             'nome': 'Dias Trabalhados',
             'un': 'dias'},
            {'item': 'headcount',
             'nome': 'Colaboradores',
             'un': 'Pessoas'},
            {'item': 'setup',
             'nome': 'Setup',
             'un': 'horas'},
            {'item': 'manutencao_corretiva',
             'nome': 'Manutenção Corretiva',
             'un': 'horas'},
            {'item': 'manutencao_preventiva',
             'nome': 'Manutenção Preventiva',
             'un': 'horas'},
        ]
        if setor.nome == "Expedição":
            opcoes.append(
                {'item': 'expedidores',
                 'nome': 'Expedidores',
                 'un': 'Pessoas'})
            opcoes.append(
                {'item': 'total_recebido',
                 'nome': 'Total Recebido',
                 'un': unidade_prod})
            opcoes.append(
                {'item': 'total_expedido',
                 'nome': 'Total Expedido',
                 'un': unidade_prod})
            opcoes.append(
                {'item': 'carga_descarga',
                 'nome': 'Carga e descarga',
                 'un': 'horas'})

        if setor.nome == "Revisão":
            opcoes.append({'item': 'revisores',
                           'nome': 'Revisores',
                           'un': 'Pessoas'}),
        if setor.nome == "Acabamento":
            opcoes.append(
                {'item': 'total_chamuscado',
                 'nome': 'Total Chamuscado',
                 'un': unidade_prod})
            opcoes.append(
                {'item': 'total_alvejado',
                 'nome': 'Total Alvejado',
                 'un': unidade_prod})
            opcoes.append(
                {'item': 'total_tingido',
                 'nome': 'Total Tingido',
                 'un': unidade_prod})
        if setor.nome == "Tecelagem":
            opcoes.append(
                {'item': 'tempo_total_atendimento',
                 'nome': 'Total Total de Atendimento',
                 'un': "horas"})
        try:
            desempenho = Desempenho.objects.get(
                periodo=periodo.id,
                setor=setor
            )
            lancado = desempenho.pk
        except:
            desempenho = ''
            lancado = False
        for opcao in opcoes:
            item = opcao['nome']
            if desempenho:
                valor = getattr(desempenho, opcao['item'])
            else:
                valor = 0
            if valor is None:
                valor = 0
            else:
                valor = int(valor)
            un = opcao['un']
            lista.append({'item': item, 'valor': valor, 'un': un})
        context['lancado'] = lancado
        context['data'] = lista
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


@method_decorator(login_required, name='dispatch')
class CustoList(ListView):
    model = Custo
    template_name = 'core/custo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        lista = []
        if setor == 0:            
            setores = Setor.objects.filter(divisao= "Têxtil")
            total = custo_setor(setor, periodo)['custo_total']
            for setor in setores:
                item = setor.nome
                valor = custo_setor(setor, periodo)['custo_total']                
                lista.append({'item': item, 'valor': valor})
            lista = sorted(lista, key=lambda x: x['valor'], reverse=True)
            setor = {
                'nome': 'Consolidado',
            }
        else:
            opcoes = (
                {'item': 'energia',
                'nome': 'Energia',
                },
                {'item': 'laboratorio',
                'nome': 'Laboratório',
                },
                {'item': 'manutencao',
                'nome': 'Manutenção',
                },
                {'item': 'mao_de_obra',
                'nome': 'Mão de Obra',
                },
                {'item': 'material_uso_continuo',
                'nome': 'Material de Uso Contínuo',
                },
                {'item': 'vapor',
                'nome': 'Vapor',
                },
                {'item': 'agua',
                'nome': 'Água',
                },
            )
            try:
                custo = Custo.objects.get(
                    periodo=periodo.id,
                    setor=setor
                )
                lancado = custo.pk
            except:
                custo = ''
                lancado = False
            total = 0
            for opcao in opcoes:
                item = opcao['nome']
                if custo:
                    valor = getattr(custo, opcao['item'])
                    total += valor
                else:
                    valor = 0
                if valor is None:
                    valor = 0                
                lista.append({'item': item, 'valor': valor})
            context['lancado'] = lancado
        context['total'] = total
        context['data'] = lista
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context

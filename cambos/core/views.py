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
from django.db import connection


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
        producao = Producao.objects.select_related('material').filter(
            setor__nome="Revisão",
            periodo=id_periodo
        )
    else:
        producao = Producao.objects.select_related('material').filter(
            setor=setor,
            periodo=id_periodo
        )
    return producao


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
    return perda


def custo_setor(setor, id_periodo):
    if setor == 0:
        custo_total = 0
        custo_lista = Custo.objects.select_related('periodo').filter(periodo=id_periodo)
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
    return custo_total


def compra_setor(setor, id_periodo):    
    if setor == 0:
        consumo = Consumo.objects.select_related('setor', 'material', 'periodo').filter(
            periodo=id_periodo,
            material__origem="Compra",
        )

    else:
        consumo = Consumo.objects.select_related('setor', 'material', 'periodo').filter(
            setor=setor,
            periodo=id_periodo,
            material__origem="Compra",
        )
    valor_compra = ValorCompra.objects.select_related('material', 'periodo').filter(            
        material__consumo__id__in = consumo,
        periodo__lte = id_periodo
    ).order_by('material','-periodo').distinct('material')

    total = 0
    
    for item in consumo:
        preco = 0
        for valor in valor_compra:
            if item.material == valor.material:
                preco = valor.valor
        total += preco * item.quantidade

    return total


def compra_insumo_setor(setor, id_periodo):    

    if setor == 0:
        material = Material.objects.filter(
            consumo__periodo = id_periodo,
            tipo = "Insumo"
        )
        consumo = Consumo.objects.select_related('material').filter(
            periodo=id_periodo,            
            material__in =material,
        )

    else:
        material = Material.objects.filter(
            consumo__setor = setor,
            consumo__periodo = id_periodo,
            tipo = "Insumo"
        )
        consumo = Consumo.objects.select_related('material').filter(
            setor=setor,
            periodo=id_periodo,            
            material__in =material,
        )
        
    valor_compra = ValorCompra.objects.prefetch_related('material').filter(            
        material__id__in = material
    ).order_by('material','-periodo').distinct('material')

    total_insumo = 0   
    preco = 0 
    for item in consumo:
        for valor in valor_compra:
            if valor.material == item.material:
                preco = valor.valor  
        total_insumo += preco * item.quantidade        

    return total_insumo


def preco_material(material, periodo):
    preco = 0    
    if material.origem == "Compra":
        valor_compra = ValorCompra.objects.select_related('material', 'periodo').filter(
            material=material,
            periodo__lte=periodo).order_by('-periodo').distinct('periodo')
        
        for valor in valor_compra:
            if valor.material == material:
                preco = valor.valor    
    else:
        setor_origem = Setor.objects.get(nome=material.origem)
        custo_setor_origem = custo_setor(setor_origem, periodo)
        compra_setor_origem = compra_setor(setor_origem, periodo)

        producao = producao_setor(setor_origem, periodo).aggregate(
            Sum('quantidade'))['quantidade__sum']
        if producao is None:
            producao = producao_setor(setor_origem, periodo.id -1).aggregate(
            Sum('quantidade'))['quantidade__sum']
        produto_interno = Consumo.objects.select_related('material').filter(
            periodo=periodo,
            setor=setor_origem,
        ).exclude(material__origem="Compra")
        preco2 = 0
        for item in produto_interno:
            setor_origem2 = Setor.objects.get(nome=item.material.origem)
            custo_setor_origem2 = custo_setor(setor_origem2, periodo)
            compra_setor_origem2 = compra_setor(setor_origem2, periodo)
            producao2 = producao_setor(setor_origem, periodo).aggregate(
                Sum('quantidade'))['quantidade__sum']
            preco2 = (custo_setor_origem2 + compra_setor_origem2) / producao2
        try:
            preco = ((custo_setor_origem + compra_setor_origem) / producao) + preco2
        except:
            preco = 0
    return preco


def preco_material_periodo(setor, id_periodo):
    total = 0
    if setor == 0:
        lista_consumo = Consumo.objects.select_related('material').filter(
            periodo=id_periodo,
            material__tipo="Material",
            material__origem="Compra"
        )
    else:
        lista_consumo = Consumo.objects.select_related('material').filter(
            setor=setor,
            periodo=id_periodo,
            material__tipo="Material"
        )
    for item in lista_consumo:
        preco = preco_material(item.material, id_periodo)
        quantidade = item.quantidade
        valor = preco * quantidade

        total += valor
    return total


def consumo_material_setor(setor, periodo):
    total = 0
    
    lista_consumo = Consumo.objects.select_related('material', 'setor').filter(
        periodo= periodo,        
    )
    
    
    valor_compra = ValorCompra.objects.select_related(
            'material'
        ).filter(periodo__id__lte = periodo.id).order_by('material','-periodo').distinct('material')

    if setor == 0:
        consumo_setor = lista_consumo.filter(material__tipo = "Material", periodo = periodo, material__origem = "Compra")
    else:
        consumo_setor = lista_consumo.filter(setor = setor, material__tipo = "Material")
    valor_compra_setor = valor_compra.filter( material__tipo = "Material")
    custo_origem = {'Entrelaçadeira':0,'Fiação':0,'Tingimento':0,'Urdideira':0,'Tecelagem':0,}
    for consumo in consumo_setor:
        preco = 0
        quantidade = 0
        if consumo.material.origem == "Compra":
            for valor in valor_compra_setor:
                if consumo.material == valor.material:
                    preco = valor.valor
            quantidade = consumo.quantidade
            valor = preco * quantidade
            total += valor
        else:         
            if custo_origem[consumo.material.origem] == 0:   
                if consumo.material.origem == "Entrelaçadeira":
                    setor_origem = 1
                elif consumo.material.origem == "Fiação":
                    setor_origem = 2
                elif consumo.material.origem == "Tingimento":
                    setor_origem = 3
                elif consumo.material.origem == "Urdideira":
                    setor_origem = 4
                else:
                    setor_origem = 5
                custo_setor_origem = custo_setor(setor_origem, periodo) #Atençãp
                producao_setor_origem = Producao.objects.filter(
                    Q(setor = setor_origem),
                    Q(periodo = periodo)|
                    Q(periodo__id = periodo.id -1)
                    ).order_by('-periodo').distinct('periodo').aggregate(
                Sum('quantidade'))['quantidade__sum'] # Atenção
                lista_consumo_origem = lista_consumo.filter(setor = setor_origem) # Atenção
                consumo_setor_origem = 0
                for consumo_externo in lista_consumo_origem: 
                    preco_externo = 0
                    quantidade_externo = 0
                    if consumo_externo.material.origem == "Compra":
                        for valor_externo in valor_compra:
                            if consumo_externo.material == valor_externo.material:
                                preco_externo = valor_externo.valor
                        quantidade_externo = consumo_externo.quantidade   
                        valor_consumo_externo = preco_externo * quantidade_externo
                        consumo_setor_origem += valor_consumo_externo
                    else:                        
                        if consumo_externo.material.origem == "Entrelaçadeira":
                            setor_origem2 = 1
                        elif consumo_externo.material.origem == "Fiação":
                            setor_origem2 = 2
                        elif consumo_externo.material.origem == "Tingimento":
                            setor_origem2 = 3
                        elif consumo_externo.material.origem == "Urdideira":
                            setor_origem2 = 4
                        else:
                            setor_origem2 = 5
                        custo_setor_origem2 = custo_setor(setor_origem2, periodo) #Atençãp
                        producao_setor_origem2 = Producao.objects.filter(
                            Q(setor = setor_origem2),
                            Q(periodo = periodo)|
                            Q(periodo__id = periodo.id -1 )
                            ).order_by('-periodo').distinct('periodo').aggregate(
                        Sum('quantidade'))['quantidade__sum'] # Atenção
                        lista_consumo_origem2 = lista_consumo.filter(setor = setor_origem2) # Atenção
                        consumo_setor_origem2 = 0
                        for consumo_externo2 in lista_consumo_origem2: 
                            preco_externo2 = 0
                            quantidade_externo2 = 0
                            if consumo_externo2.material.origem == "Compra":
                                for valor_externo2 in valor_compra:
                                    if consumo_externo2.material == valor_externo2.material:
                                        preco_externo2 = valor_externo2.valor
                                quantidade_externo2 = consumo_externo2.quantidade   
                                valor_consumo_externo2 = preco_externo2 * quantidade_externo2
                                consumo_setor_origem2 += valor_consumo_externo2
                        try:
                            preco_unitario_setor2 = (consumo_setor_origem2 + custo_setor_origem2) / producao_setor_origem2
                        except:
                            preco_unitario_setor2 = 0
                        quantidade_externo = consumo_externo.quantidade 
                        valor2 = preco_unitario_setor2 * quantidade_externo                           
                        consumo_setor_origem += valor2   
                try:                          
                    preco_unitario_setor = (consumo_setor_origem + custo_setor_origem) / producao_setor_origem
                except:
                    preco_unitario_setor = 0
                quantidade = consumo.quantidade
                valor3 = preco_unitario_setor * quantidade
                custo_origem[consumo.material.origem] = preco_unitario_setor
                total += valor3
            else:
                total += custo_origem[consumo.material.origem] * consumo.quantidade
    return total

#Arquivo
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
    label_total = []
    total_gastos = 0
    while (p_fim < 12):
        p_fim += 1
        label_periodo.append(meses_abr[p_inicio])

        producao = producao_setor(setor, id_periodo).aggregate(
            Sum('quantidade'))['quantidade__sum']
        if not producao:
            producao = 0
        try:
            insumo = compra_insumo_setor(setor, id_periodo) / producao
        except:
            insumo = 0
        try:
            custo = custo_setor(setor, id_periodo) / producao
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
        total_gastos = insumo + material + custo
        label_total.append(f'{meses_abr[p_inicio]} - R$ {round(total_gastos, 2)}')
        id_periodo += 1
        if p_inicio == 11:
            p_inicio = 0
        else:
            p_inicio += 1

    return {
        'label': label_periodo,
        'label_total': label_total,
        'producao': prod_periodo,
        'insumo': insumo_periodo,
        'material': material_periodo,
        'custo': custo_periodo
    }


def dash2(nome_periodo, periodo, setor):
    meses_abr = ["Jan", "fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    periodo_ind = meses_abr.index(nome_periodo[0:3])
    if periodo_ind == 11:
        p_inicio = 0
    else:
        p_inicio = periodo_ind + 1
    p_fim = 0    
    id_periodo = periodo.id
    id_periodo -= 11
    label_periodo = []
    prod_periodo = []
    insumo_periodo = []
    material_periodo = []
    custo_periodo = []
    capita_periodo = []
    
    if setor == 0:
        desempenho = Desempenho.objects.select_related('setor', 'periodo').filter(
            Q(periodo__id__gte = id_periodo) ,
            Q(periodo__id__lte = id_periodo + 11)    
        )

        producao_ano = Producao.objects.filter(        
            Q(setor__nome = "Revisão"),
            Q(periodo__id__gte = id_periodo) ,
            Q(periodo__id__lte = id_periodo + 11)    
        ).values('periodo').order_by('periodo').annotate(total=Sum('quantidade'))

        insumo_consumido = Consumo.objects.select_related('material', 'periodo').filter( 
            Q(material__tipo = "Insumo"),           
            Q(periodo__id__gte = id_periodo) ,
            Q(periodo__id__lte = id_periodo + 11)    
        ).values('material', 'periodo', 'quantidade')

        valor_compra_insumo = ValorCompra.objects.prefetch_related('material', 'periodo').filter(            
            Q(material__tipo = "Insumo"),                       
            Q(periodo__id__lte = id_periodo + 11),
        ).values('material', 'periodo', 'valor')
        
    else:
        
        desempenho = Desempenho.objects.select_related('setor', 'periodo').filter(
            Q(periodo__id__gte = id_periodo) ,
            Q(periodo__id__lte = id_periodo + 11)    
        )
        producao_ano = Producao.objects.filter(        
            Q(setor = setor),
            Q(periodo__id__gte = id_periodo),
            Q(periodo__id__lte = id_periodo + 11)    
        ).values('periodo').order_by('periodo').annotate(total=Sum('quantidade'))

        
        insumo_consumido = Consumo.objects.prefetch_related('material', 'periodo').filter(
            Q(setor = setor),
            Q(material__tipo = "Insumo"),           
            Q(periodo__id__gte = id_periodo) ,
            Q(periodo__id__lte = id_periodo + 11),
        ).values('material', 'periodo', 'quantidade')

        valor_compra_insumo = ValorCompra.objects.prefetch_related('material', 'periodo').filter(            
            Q(material__tipo = "Insumo"),                       
            Q(periodo__id__lte = id_periodo + 11),
        ).values('material', 'periodo', 'valor')

    percapita_total = desempenho.values('periodo').order_by('periodo').annotate(total=Sum('headcount'))
    while (p_fim < 12):
        p_fim += 1
        label_periodo.append(meses_abr[p_inicio])
        producao = 0
        insumo_total = 0
        percapita = 0
        for mes in producao_ano:            
            if mes['periodo'] == id_periodo:                
                producao = mes['total']
                for insumo in insumo_consumido:                    
                    if insumo['periodo'] == mes['periodo']:
                        for valor in valor_compra_insumo:                
                            if valor["material"] == insumo['material'] and valor['periodo'] == insumo['periodo']:
                                
                                preco = float(valor['valor'])
                                quantidade = insumo['quantidade']
                                total = preco * quantidade
                                insumo_total += total
                for pessoa in percapita_total:
                    if pessoa['periodo'] == mes['periodo']:
                        percapita = producao / pessoa['total']
                try:
                    insumo_total = insumo_total / producao                                                       
                except:
                    pass
        capita_periodo.append(int(percapita))
        insumo_periodo.append(round(insumo_total,2))
        prod_periodo.append(int(producao))
                

        try:
            custo = custo_setor(setor, id_periodo) / producao
        except:
            custo = 0
            
        try:
            periodo2 = Periodo.objects.get(id = id_periodo)
            material = consumo_material_setor(setor, periodo2) / producao
        except:
            material = 0
        
        
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
        'custo': custo_periodo,        
        'percapita': capita_periodo,        
    }


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Periodo
        try:
            periodo = Periodo.objects.get(nome=self.request.GET.get('periodo', None))
        except:
            periodo = Periodo.objects.latest('periodo')

        # Setor
        try:
            setor = Setor.objects.get(id=self.request.GET.get('setor', None))
        except:
            setor = 0

        if not setor or setor == 0:
            unidades = 'Metros'
            unidade = 'Metro'

        elif setor.id < 5:
            unidades = 'Quilos'
            unidade = 'Quilo'
        else:
            unidades = 'Metros'
            unidade = 'Metro'

        #Produção
        producao = producao_setor(setor, periodo)
        
        producao_total = producao.aggregate(
                Sum('quantidade')
            )['quantidade__sum']

        #Desempenho
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
            
            eficiencia = (producao_total/ total_planejado) * 100
        except:            
            eficiencia = 0

        custo = custo_setor(setor, periodo)
        try:
            custo_un = custo / producao_total
        except:
            custo_un = 0

        #Perda
        perda = perda_setor(setor, periodo).aggregate(
            Sum('quantidade'))['quantidade__sum']
        try:
            perda_un = (perda / producao_total) * 100
        except:
            perda_un = 0

        #Insumo
        insumo = compra_insumo_setor(setor, periodo)
        try:
            insumo_un = insumo / producao_total
        except:
            insumo_un = 0

        #Material
        valor_consumo_material = consumo_material_setor(setor, periodo)
        try:
            materia_prim_un = valor_consumo_material / producao_total
        except:
            materia_prim_un = 0

        dashboard = dash2(periodo.nome, periodo, setor)
        if setor == 0:
            setor = {'nome': 'Consolidado'}
        
       
        #dash
        
        context['data1'] = dashboard['producao']
        context['data2'] = dashboard['custo']
        context['data3'] = dashboard['insumo']
        context['data4'] = dashboard['material']
        context['data5'] = dashboard['percapita']
        context['labels1'] = dashboard['label']
        #context['contagem'] = len(connection.queries)
        context['setor'] = setor
        context['periodo'] = periodo.nome
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = producao_total
        context['eficiencia'] = eficiencia
        context['custo'] = custo_un
        context['perda'] = perda_un
        context['insumo'] = insumo_un
        context['materia_prima'] = materia_prim_un

        return context

##Arquivo
@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
            
        if not setor or setor == 0:
            unidades = 'Metros'
            unidade = 'Metro'

        elif setor.id < 5:
            unidades = 'Quilos'
            unidade = 'Quilo'
        else:
            unidades = 'Metros'
            unidade = 'Metro'

        producao = producao_setor(setor, periodo.id)
        producao_total = producao.aggregate(
                Sum('quantidade')
            )['quantidade__sum']
    
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
            
            eficiencia = (producao_total/ total_planejado) * 100
        except:            
            eficiencia = 0

        custo = custo_setor(setor, periodo)
        try:
            custo_un = custo / producao_total
        except:
            custo_un = 0

        perda = perda_setor(setor, periodo).aggregate(
            Sum('quantidade'))['quantidade__sum']
        try:
            perda_un = (perda / producao_total) * 100
        except:
            perda_un = 0

        insumo = compra_insumo_setor(setor, periodo)
        try:
            insumo_un = insumo / producao_total
        except:
            insumo_un = 0

        valor_consumo_material = preco_material_periodo(setor, periodo)
        try:
            materia_prim_un = valor_consumo_material / producao_total
        except:
            materia_prim_un = 0

        dashboard = dash(periodo.nome, periodo.id, setor)
        if setor == 0:
            setor = {'nome': 'Consolidado'}

        context['contagem'] = len(connection.queries)
        context['materia_prima'] = materia_prim_un
        context['insumo'] = insumo_un
        context['perda'] = perda_un
        context['custo'] = custo_un
        context['eficiencia'] = eficiencia
        context['unidade'] = unidade
        context['unidades'] = unidades
        context['producao'] = producao_total
        context['periodo'] = periodo.nome
        context['setor'] = setor
        #dash
        context['data1'] = dashboard['producao']
        context['data2'] = dashboard['custo']
        context['data3'] = dashboard['insumo']
        context['data4'] = dashboard['material']
        context['labels1'] = dashboard['label']
        return context

@method_decorator(login_required, name='dispatch')
class ProducaoList(ListView):
    model = Producao
    template_name = 'core/producao_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = get_periodo(self)
        setor = get_setor(self)
        producao = producao_setor(setor, periodo.id)
        total = producao.aggregate(
            Sum('quantidade'))['quantidade__sum']
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
            for item in producao.distinct('material'):
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
        perda = perda_setor(setor.id, periodo.id)
        total = perda.aggregate(
            Sum('quantidade'))['quantidade__sum']
        if setor.id < 5:
            unidades = 'Quilos'
            unidade = 'kg'
        else:
            unidades = 'Metros'
            unidade = 'm'
        lista = []
        historico = Perda.objects.filter(
            setor=setor.id,
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
        total = consumo_material_setor(setor, periodo)
        valor = 0
        if setor == 0:
            consumo = Consumo.objects.select_related('material', 'periodo', 'setor').filter(
                periodo=periodo.id,
                material__tipo="Material",
                material__origem="Compra"
            )                        

            for item in consumo:
                quantidade = 0
                percentual = 0
                valor = 0
                material_nome = item.material.nome
                material_unidade = item.material.unidade
                origem = item.material.origem                
                preco = preco_material(item.material, periodo)                                
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
            
            historico = Consumo.objects.select_related('setor','material', 'periodo').filter(
                Q(setor=setor),
                Q(material__tipo="Material"),
                Q(periodo__id__gte= periodo.id - 2),
                Q(periodo__id__lte= periodo.id)                
            ).order_by('material', '-periodo').distinct('material')        
                    
            for item in historico:
                material_nome = item.material.nome
                material_unidade = item.material.unidade
                origem = item.material.origem
                quantidade = 0
                percentual = 0
                valor = 0
                id_consumo = ''

                preco = preco_material(item.material, periodo) 
                if item.periodo == periodo:
                    quantidade = item.quantidade
                    id_consumo = item.id                
                    valor = quantidade * preco
                    try:
                        percentual = (valor / total)*100
                    except:
                        percentual = 0
                
                id_material = item.material.id
                                
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
        #context['contagem'] = len(connection.queries)        
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
                periodo=periodo.id,
                material__tipo="Insumo",
            )            
            for item in consumo:
                quantidade = item.quantidade
                preco = preco_material(item.material, periodo)
                valor = quantidade * preco
                total += valor

            for item in consumo:                
                percentual = 0                
                material_nome = item.material.nome                
                preco = preco_material(item.material, periodo)                                
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
                preco = preco_material(consumido.material, periodo)
                valor = quantidade * preco
                total += valor

            for item in historico:
                material_nome = item.material.nome
                quantidade = 0
                preco = preco_material(item.material, periodo)
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
            total = custo_setor(setor, periodo)
            for setor in setores:
                item = setor.nome
                valor = custo_setor(setor, periodo)             
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

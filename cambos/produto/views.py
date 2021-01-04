from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import (
    Producao,
    Material,
    Desempenho,
    Consumo
)
from core.models import (
    Setor,
    Periodo,
)
from .form import (
    MaterialProducaoForm,
    ProducaoModalForm,
    ProducaoForm,
    DesempenhoForm,
    ConsumoForm,
    ConsumoModalForm,
    MaterialConsumoForm
)

def get_periodo(self):
    try:
        periodo = Periodo.objects.get(nome = self.request.GET.get('periodo', None))
    except:
        periodo = Periodo.objects.latest('periodo')
    return periodo

def get_setor(self):
    try:
        setor = Setor.objects.get(id = self.request.GET.get('setor', None))
    except:
        setor = Setor.objects.get(id=7)
    return setor


class ProducaoModalCreate(CreateView):
    model = Producao
    form_class = ProducaoModalForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        material = Material.objects.get(id = self.kwargs['pk'])
        periodo = get_periodo(self)
        setor = get_setor(self)        
        context['item'] = material.nome
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(ProducaoModalCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)
        material = Material.objects.get(id = self.kwargs['pk'])
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo
        initial['material'] = material
        return initial


class ProducaoCreate(CreateView):
    model = Producao
    form_class = ProducaoForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_form_kwargs(self):
        periodo = get_periodo(self)
        setor = get_setor(self)
        kwargs = super().get_form_kwargs()
        produzidos = Producao.objects.filter(
            periodo = periodo.id,
            setor = setor.id
        ).values('material__id')
        kwargs['produzidos'] = produzidos
        return kwargs
    
    def get_initial(self, *args, **kwargs):
        initial = super(ProducaoCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)        
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo        
        return initial


class ProducaoModalUpdate(UpdateView):
    model = Producao
    form_class = ProducaoModalForm
    
    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material.nome
        context['item'] = item
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


class ProducaoDelete(DeleteView):
    model = Producao 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material.nome
        context['item'] = item
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context   

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/producao_list' + f'?setor={setor.id}&periodo={periodo.nome}'


class ProducaoMaterialCreate(CreateView):
    model = Material
    form_class = MaterialProducaoForm
    template_name = "produto/producao_material_create.html"

    def get_success_url(self, **kwargs):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        pk = self.object.pk
        return f'/produto/producao_modal_create/{pk}' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                
        context['tipo'] = "Material"
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
        
    def get_initial(self, *args, **kwargs):        
        initial = super(ProducaoMaterialCreate, self).get_initial(**kwargs)              
        setor = get_setor(self)        
        if setor.id < 5:
            origem = setor.nome
            unidade = 'kg'
        else:
            origem = "Tecelagem"
            unidade = "m"
        initial['unidade'] = unidade
        initial['tipo'] = 'Material'
        initial['origem'] = origem        
        return initial


class DesempenhoCreate(CreateView):
    model = Desempenho
    form_class = DesempenhoForm

    def get_success_url(self, **kwargs):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/desempenho_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                        
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
        
    def get_initial(self, *args, **kwargs):                
        initial = super(DesempenhoCreate, self).get_initial(**kwargs)   
        setor = get_setor(self)   
        periodo = get_periodo(self)
        desempenho = Desempenho.objects.filter(setor = setor.id)                   
        ultimo_desempenho = desempenho.latest('periodo')
        initial['setor'] = setor.id
        initial['periodo'] = periodo.id                
        initial['capacidade_total'] = ultimo_desempenho.capacidade_total        
        initial['total_planejado'] = ultimo_desempenho.total_planejado        
        initial['headcount'] = ultimo_desempenho.headcount        
        return initial


class DesempenhoUpdate(UpdateView):
    model = Desempenho
    form_class = DesempenhoForm
    
    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/desempenho_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


class ConsumoModalCreate(CreateView):
    model = Consumo
    form_class = ConsumoModalForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_material_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        material = Material.objects.get(id = self.kwargs['pk'])
        periodo = get_periodo(self)
        setor = get_setor(self)        
        context['item'] = material.nome
        context['tipo'] = material.tipo
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(ConsumoModalCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)
        material = Material.objects.get(id = self.kwargs['pk'])
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo
        initial['material'] = material
        return initial


class ConsumoCreate(CreateView):
    model = Consumo
    form_class = ConsumoForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_material_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                
        context['periodo'] = periodo.nome
        context['setor'] = setor
        context['tipo'] = "Material"
        return context
    
    def get_form_kwargs(self):
        periodo = get_periodo(self)
        setor = get_setor(self)
        kwargs = super().get_form_kwargs()
        consumidos = Consumo.objects.filter(
            material__tipo = "Material",
            periodo = periodo.id,
            setor = setor.id
        ).values('material__id')
        kwargs['material_tipo'] = "Material"
        kwargs['consumidos'] = consumidos
        return kwargs
    
    def get_initial(self, *args, **kwargs):
        initial = super(ConsumoCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)        
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo        
        return initial


class ConsumoModalUpdate(UpdateView):
    model = Consumo
    form_class = ConsumoModalForm
    
    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_material_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material
        context['item'] = item.nome
        context['tipo'] = item.tipo
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


class ConsumoDelete(DeleteView):
    model = Consumo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material.nome
        context['item'] = item
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context   

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_material_list' + f'?setor={setor.id}&periodo={periodo.nome}'


class MaterialConsumoCreate(CreateView):
    model = Material
    form_class = MaterialConsumoForm
    template_name = "produto/material_consumo_create.html"

    def get_success_url(self, **kwargs):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        pk = self.object.pk
        return f'/produto/consumo_modal_create/{pk}' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                
        context['tipo'] = "Material"
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_initial(self, *args, **kwargs):        
        initial = super(MaterialConsumoCreate, self).get_initial(**kwargs)                      
        initial['tipo'] = 'Material'           
        return initial


class InsumoModalCreate(CreateView):
    model = Consumo
    form_class = ConsumoModalForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_insumo_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        material = Material.objects.get(id = self.kwargs['pk'])
        periodo = get_periodo(self)
        setor = get_setor(self)        
        context['tipo'] = material.tipo
        context['item'] = material.nome
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(InsumoModalCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)
        material = Material.objects.get(id = self.kwargs['pk'])
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo
        initial['material'] = material
        return initial


class InsumoCreate(CreateView):
    model = Consumo
    form_class = ConsumoForm

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_insumo_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                
        context['periodo'] = periodo.nome
        context['setor'] = setor
        context['tipo'] = "Insumo"
        return context
    
    def get_form_kwargs(self):
        periodo = get_periodo(self)
        setor = get_setor(self)
        kwargs = super().get_form_kwargs()
        consumidos = Consumo.objects.filter(
            material__tipo = "Insumo",
            periodo = periodo.id,
            setor = setor.id
        ).values('material__id')
        kwargs['material_tipo'] = "Insumo"
        kwargs['consumidos'] = consumidos
        return kwargs
    
    def get_initial(self, *args, **kwargs):
        initial = super(InsumoCreate, self).get_initial(**kwargs)
        periodo = get_periodo(self)        
        setor = get_setor(self)        
        initial['setor'] = setor
        initial['periodo'] = periodo        
        return initial


class InsumoModalUpdate(UpdateView):
    model = Consumo
    form_class = ConsumoModalForm
    
    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_insumo_list' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material
        context['item'] = item.nome
        context['tipo'] = item.tipo
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context


class InsumoDelete(DeleteView):
    model = Consumo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        periodo = get_periodo(self)
        setor = get_setor(self)        
        item = self.object.material.nome
        context['item'] = item
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context   

    def get_success_url(self):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        return '/core/consumo_insumo_list' + f'?setor={setor.id}&periodo={periodo.nome}'


class MaterialInsumoCreate(CreateView):
    model = Material
    form_class = MaterialConsumoForm
    template_name = "produto/insumo_consumo_create.html"

    def get_success_url(self, **kwargs):
        periodo = get_periodo(self)
        setor = get_setor(self)   
        pk = self.object.pk
        return f'/produto/insumo_modal_create/{pk}' + f'?setor={setor.id}&periodo={periodo.nome}'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)                
        periodo = get_periodo(self)
        setor = get_setor(self)                
        context['tipo'] = "Insumo"
        context['periodo'] = periodo.nome
        context['setor'] = setor
        return context
    
    def get_initial(self, *args, **kwargs):        
        initial = super(MaterialInsumoCreate, self).get_initial(**kwargs)                      
        initial['tipo'] = 'Insumo'           
        initial['origem'] = 'Compra'           
        return initial

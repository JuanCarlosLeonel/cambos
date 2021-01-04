from django.urls import path
from django.conf.urls import include, url
from . import views
from core.views import(
    Index,
    ProducaoList,
    DesempenhoList,
    UserCreate,
    ConsumoMaterialList,
    ConsumoInsumoList,
    CustoList,
    PerdaList
)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_create/', UserCreate.as_view(), name = 'user_create_cbv'),
    #index       
    path('', Index.as_view(), name='core_index'),
    path('producao_list',  ProducaoList.as_view(), name='producao_list'),
    path('consumo_material_list',  ConsumoMaterialList.as_view(), name='consumo_material_list'),
    path('consumo_insumo_list',  ConsumoInsumoList.as_view(), name='consumo_insumo_list'),
    path('desempenho_list',  DesempenhoList.as_view(), name='desempenho_list'),
    path('custo_list',  CustoList.as_view(), name='custo_list'),    
    path('perda_list',  PerdaList.as_view(), name='perda_list'),    
]

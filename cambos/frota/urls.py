from django.urls import path
from django.views.generic.base import View
from .views import(
    Index,
    VeiculoIndex,
    ViagemList,
    ViagemCreate,
    ViagemUpdate,
    ViagemDelete,    
    AbastecimentoList,
    AbastecimentoCreate,
    AbastecimentoUpdate,
    AbastecimentoDelete,
    VeiculoList,    
)

urlpatterns = [
    path('index', Index.as_view(), name='frota_index'),        
    path('veiculo_index/<str:pk>/', VeiculoIndex.as_view(), name='veiculo_index'),        
    path('viagem_list/<str:pk>/',  ViagemList.as_view(), name='viagem_list'),
    path('viagem_create/<str:pk>/', ViagemCreate.as_view(), name = 'viagem_create'),
    path('viagem_update/<str:pk>/', ViagemUpdate.as_view(), name='viagem_update'),    
    path('viagem_delete/<int:pk>/',ViagemDelete.as_view(), name='viagem_delete_cbv'),
    path('abastecimento_list',  AbastecimentoList.as_view(), name='abastecimento_list'),
    path('abastecimento_create/', AbastecimentoCreate.as_view(), name = 'abastecimento_create'),
    path('abastecimento_update/<str:pk>/', AbastecimentoUpdate.as_view(), name='abastecimento_update'),    
    path('abastecimento_delete/<int:pk>/',AbastecimentoDelete.as_view(), name='abastecimento_delete_cbv'),
    path('veiculo_list',  VeiculoList.as_view(), name='veiculo_list'),
]
    
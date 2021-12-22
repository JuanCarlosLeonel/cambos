from django.urls import path
from django.views.generic.base import View
from .views import(
    Index,
    ViagemList,
    ViagemCreate,
    ViagemUpdate,
    ViagemDelete,
    CorridaList,
    CorridaCreate,
    AbastecimentoList,
    AbastecimentoCreate,
    AbastecimentoUpdate,
    AbastecimentoDelete
)

urlpatterns = [
    path('index', Index.as_view(), name='frota_index'),    
    path('viagem_list',  ViagemList.as_view(), name='viagem_list'),
    path('viagem_create/', ViagemCreate.as_view(), name = 'viagem_create'),
    path('viagem_update/<str:pk>/', ViagemUpdate.as_view(), name='viagem_update'),    
    path('viagem_delete/<int:pk>/',ViagemDelete.as_view(), name='viagem_delete_cbv'),
    path('corrida_list',  CorridaList.as_view(), name='corrida_list'),
    path('corrida_create/', CorridaCreate.as_view(), name = 'corrida_create'),
    path('abastecimento_list',  AbastecimentoList.as_view(), name='abastecimento_list'),
    path('abastecimento_create/', AbastecimentoCreate.as_view(), name = 'abastecimento_create'),
    path('abastecimento_update/<str:pk>/', AbastecimentoUpdate.as_view(), name='abastecimento_update'),    
    path('abastecimento_delete/<int:pk>/',AbastecimentoDelete.as_view(), name='abastecimento_delete_cbv'),
]
    
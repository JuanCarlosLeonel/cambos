from django.urls import path
from django.conf.urls import include, url
from . import views
from .views import(
    Index,
    CalendarioTemplate,
    ProducaoRoupaList,
    ConfeccaoList,
    ConfeccaoDetail,
    ProgramacaoList,
    PedidoDetail

)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
    path('calendario/<int:pk>/', CalendarioTemplate.as_view(), name='calendario'),    
    path('producao_roupa_list',  ProducaoRoupaList.as_view(), name='producao_roupa_list'),
    path('programacao_list',  ProgramacaoList.as_view(), name='programacao_list'),
    path('confeccao_list',  ConfeccaoList.as_view(), name='confeccao_list'),
    path('confeccao_detail/<int:pk>/',ConfeccaoDetail.as_view(), name='confeccao_detail_cbv'),
    path('pedido_detail/<int:pk>/',PedidoDetail.as_view(), name='pedido_detail'),
]

from django.urls import path
from django.conf.urls import include, url
from django.views.generic.base import View
from .views import(
    Index,
    CalendarioTemplate,
    ProducaoRoupaList,
    ConfeccaoList,
    ConfeccaoDetail,
    ProgramacaoList,
    PedidoDetail,
    PedidoCreate,
    PedidoUpdate,
    PedidoUpdateTag,
    TagCreate,
    PcpList,
    PcpUpdate,
    ListPcpUpdate,
    CreateOficina,
    UpdateOficina,
    UpdateAPI,

)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
    path('calendario/<int:pk>/', CalendarioTemplate.as_view(), name='calendario'),    
    path('producao_roupa_list',  ProducaoRoupaList.as_view(), name='producao_roupa_list'),
    path('programacao_list',  ProgramacaoList.as_view(), name='programacao_list'),
    path('confeccao_list',  ConfeccaoList.as_view(), name='confeccao_list'),
    path('confeccao_detail/<int:pk>/',ConfeccaoDetail.as_view(), name='confeccao_detail_cbv'),
    path('pedido_detail/<int:pk>/',PedidoDetail.as_view(), name='pedido_detail'),
    path('pedido_create/<int:pk>/',PedidoCreate.as_view(), name='pedido_create'),
    path('pedido_update/<int:pk>/',PedidoUpdate.as_view(), name='pedido_update'),
    path('tag_createpedido/<int:pk>/',PedidoUpdateTag.as_view(), name='tag_createpedido'),
    path('tag_create/<int:pk>/',TagCreate.as_view(), name='tag_create'),
    path('oficina_create/', CreateOficina.as_view(), name='oficina_create'),
    path('oficina_update/<int:pk>/', UpdateOficina.as_view(), name='oficina_update'),
    path('pcp_update/<int:pk>/<str:pk2>/',PcpUpdate.as_view(), name='pcp_update'),
    path('pcp_list/<int:pk>/',PcpList.as_view(), name='pcp_list'),
    path('list_pcp_update/<int:pk>/',ListPcpUpdate.as_view(), name='list_pcp_update'),
    path('update_api/',UpdateAPI, name='update_api'),
]

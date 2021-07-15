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
    PedidoUpdate,
    TagCreate,
    CreateOficina,
    UpdateOficina,

)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
    path('calendario/<int:pk>/', CalendarioTemplate.as_view(), name='calendario'),    
    path('producao_roupa_list',  ProducaoRoupaList.as_view(), name='producao_roupa_list'),
    path('programacao_list',  ProgramacaoList.as_view(), name='programacao_list'),
    path('confeccao_list',  ConfeccaoList.as_view(), name='confeccao_list'),
    path('confeccao_detail/<int:pk>/',ConfeccaoDetail.as_view(), name='confeccao_detail_cbv'),
    path('pedido_detail/<int:pk>/',PedidoDetail.as_view(), name='pedido_detail'),
    path('pedido_update/<int:pk>/',PedidoUpdate.as_view(), name='pedido_update'),
    path('tag_create/<int:pk>/',TagCreate.as_view(), name='tag_create'),
    path('oficina_create/', CreateOficina.as_view(), name='oficina_create'),
    path('oficina_update/<int:pk>/', UpdateOficina.as_view(), name='oficina_update'),
]

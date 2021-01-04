from django.urls import path
from django.conf.urls import include, url
from . import views
from produto.views import(
    ProducaoModalCreate,
    ProducaoCreate,
    ProducaoModalUpdate,
    ProducaoDelete,
    ProducaoMaterialCreate,
    DesempenhoCreate,
    DesempenhoUpdate,
    ConsumoModalCreate,
    ConsumoModalUpdate,
    ConsumoCreate,
    ConsumoDelete,
    MaterialConsumoCreate    
)

urlpatterns = [
    path("select2/", include("django_select2.urls")),

    path('producao_material_create', ProducaoMaterialCreate.as_view(), name = 'producao_material_create'),
    path('producao_modal_create/<str:pk>/', ProducaoModalCreate.as_view(), name = 'producao_modal_create'),
    path('producao_create/', ProducaoCreate.as_view(), name = 'producao_create'),
    path('producao_modal_update/<str:pk>/', ProducaoModalUpdate.as_view(), name = 'producao_modal_update'),
    path('producao_delete/<int:pk>/',ProducaoDelete.as_view(), name='producao_delete_cbv'),
    

    path('material_consumo_create', MaterialConsumoCreate.as_view(), name = 'material_consumo_create'),
    path('consumo_modal_create/<str:pk>/', ConsumoModalCreate.as_view(), name = 'consumo_modal_create'),
    path('consumo_material_create/', ConsumoCreate.as_view(), name = 'consumo_material_create'),    
    path('consumo_modal_update/<str:pk>/', ConsumoModalUpdate.as_view(), name = 'consumo_modal_update'),
    path('consumo_delete/<int:pk>/',ConsumoDelete.as_view(), name='consumo_delete_cbv'),
   
    path('desempenho_create/', DesempenhoCreate.as_view(), name = 'desempenho_create'),
    path('desempenho_update/<str:pk>/', DesempenhoUpdate.as_view(), name = 'desempenho_update'),
    
]
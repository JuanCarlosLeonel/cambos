from django.urls import path
from django.conf.urls import include, url
from . import views
from produto.views import(
    ProducaoModalCreate,
    ProducaoCreate,
    ProducaoModalUpdate,
    ProducaoDelete,
    MaterialProducaoCreate,
)

urlpatterns = [
    path('material_producao_create', MaterialProducaoCreate.as_view(), name = 'material_producao_create'),
    path('producao_modal_create/<str:pk>/', ProducaoModalCreate.as_view(), name = 'producao_modal_create'),
    path('producao_create/', ProducaoCreate.as_view(), name = 'producao_create'),
    path('producao_modal_update/<str:pk>/', ProducaoModalUpdate.as_view(), name = 'producao_modal_update'),
    path('producao_delete/<int:pk>/',ProducaoDelete.as_view(), name='producao_delete_cbv'),
    path("select2/", include("django_select2.urls")),
]
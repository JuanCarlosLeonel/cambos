from django.urls import path
from django.conf.urls import include, url
from . import views
from produto.views import(
    ProducaoModalCreate,
    ProducaoModalUpdate,
    ProducaoDelete
)

urlpatterns = [
    path('producao_modal_create/<str:pk>/', ProducaoModalCreate.as_view(), name = 'producao_modal_create'),
    path('producao_modal_update/<str:pk>/', ProducaoModalUpdate.as_view(), name = 'producao_modal_update'),
    path('producao_delete/<int:pk>/',ProducaoDelete.as_view(), name='producao_delete_cbv'),
]
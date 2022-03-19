from django.urls import path
from django.views.generic.base import View
from .views import(
    Index,
    PlanoAcaoCreate,    
    QualidadeDetail,
    PlanoAcaoCreate,
    PlanoAcaoDetail,
    AcaoCreate,
    AcaoUpdate,
    AcaoList
)

urlpatterns = [
    path('index', Index.as_view(), name='qualidade_index'),        
    path('qualidade_detail/<int:pk>/',QualidadeDetail.as_view(), name='qualidade_detail'),
    path('plano_acao_create/<int:pk>/',PlanoAcaoCreate.as_view(), name='plano_acao_create'),
    path('acao_create/<int:pk>/',AcaoCreate.as_view(), name='acao_create'),
    path('acao_update/<int:pk>/',AcaoUpdate.as_view(), name='acao_update'),
    path('plano_acao_detail/<int:pk>/',PlanoAcaoDetail.as_view(), name='plano_acao_detail'),
    path('acao_list', AcaoList.as_view(), name='acao_list'),        
]

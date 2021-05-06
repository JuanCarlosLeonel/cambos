from django.urls import path
from django.conf.urls import include, url
from . import views
from roupa.views import(
    Index,
    ProducaoList
)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
    path('producao_list',  ProducaoList.as_view(), name='producao_list'),
]

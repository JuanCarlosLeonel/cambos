from django.urls import path
from django.conf.urls import include, url
from . import views
from .views import(
    Index,
    CalendarioTemplate,
    ProducaoRoupaList,
    OficinaList
)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
    path('calendario/<int:pk>/', CalendarioTemplate.as_view(), name='calendario'),    
    path('producao_roupa_list',  ProducaoRoupaList.as_view(), name='producao_roupa_list'),
    path('oficina_list',  OficinaList.as_view(), name='oficina_list'),
]

from django.urls import path
from django.conf.urls import include, url
from . import views
from roupa.views import(
    Index,
    CalendarioTemplate,
    ProducaoRoupaList
)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
    path('calendario/<int:pk>/', CalendarioTemplate.as_view(), name='calendario'),    
    path('producao_roupa_list',  ProducaoRoupaList.as_view(), name='producao_roupa_list'),
]

from django.urls import path
from django.conf.urls import include, url
from . import views
from core.views import(
    Index,
    ProducaoList
)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #index       
    path('', Index.as_view(), name='core_index'),
    path('producao_list',  ProducaoList.as_view(), name='producao_list'),
]

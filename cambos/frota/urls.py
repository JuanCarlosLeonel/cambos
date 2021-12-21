from django.urls import path
from django.views.generic.base import View
from .views import(
    Index,
    ViagemList
)

urlpatterns = [
    path('index', Index.as_view(), name='frota_index'),    
    path('viagem_list',  ViagemList.as_view(), name='viagem_list'),
]
    
from django.urls import path
from django.views.generic.base import View
from .views import(
    Index,    
    QualidadeDetail

)

urlpatterns = [
    path('index', Index.as_view(), name='qualidade_index'),        
    path('qualidade_detail/<int:pk>/',QualidadeDetail.as_view(), name='qualidade_detail'),
]

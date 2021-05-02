from django.urls import path
from django.conf.urls import include, url
from . import views
from roupa.views import(
    Index,
)

urlpatterns = [
    path('index', Index.as_view(), name='roupa_index'),    
]

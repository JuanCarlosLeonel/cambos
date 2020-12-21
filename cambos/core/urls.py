from django.urls import path
from django.conf.urls import include, url
from . import views
from core.views import(
    Index,
    TextilP
)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #index       
    path('', Index.as_view(), name='core_index'),
    path('textilp/<str:pk>/', Index.as_view(), name='core_textilp'),
]

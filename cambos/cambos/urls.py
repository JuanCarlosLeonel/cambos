from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('core.urls')),
    path('core/', include('core.urls')),    
    path('roupa/', include('roupa.urls')),    
    path('frota/', include('frota.urls')),    
    path('produto/', include('produto.urls')),    
    path('qualidade/', include('qualidade.urls')),    
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('select2/', include('django_select2.urls')),
]

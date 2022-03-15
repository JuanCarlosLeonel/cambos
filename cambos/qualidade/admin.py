from django.contrib import admin
from .models import (    
    Auditor,
    TabelaAmostragem,
    ItemTabelaAmostragem,
    Inspecao
)

admin.site.register(Auditor)
admin.site.register(TabelaAmostragem)
admin.site.register(ItemTabelaAmostragem)
admin.site.register(Inspecao)


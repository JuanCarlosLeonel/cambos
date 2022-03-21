from django.contrib import admin
from .models import (    
    Auditor,
    TabelaAmostragem,
    ItemTabelaAmostragem,
    Inspecao,
    Acao,
    PlanoDeAcao,
    QualidadeBot,
    QualidadeTrack
)

admin.site.register(Auditor)
admin.site.register(TabelaAmostragem)
admin.site.register(ItemTabelaAmostragem)
admin.site.register(Inspecao)
admin.site.register(Acao)
admin.site.register(PlanoDeAcao)
admin.site.register(QualidadeBot)
admin.site.register(QualidadeTrack)


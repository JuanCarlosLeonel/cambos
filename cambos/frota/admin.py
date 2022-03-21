from django.contrib import admin

from .models import (
    Veiculo,
    Viagem,
    Abastecimento,    
    Infracao,
    Seguro,
    Rastreio,
    DespesaViagem,
    FrotaPermissao,
    Manutencao,
    Motorista,
    ItemViagem,
    FrotaBot,
    SolicitacaoViagem,
)

admin.site.register(Veiculo)
admin.site.register(Viagem)
admin.site.register(Abastecimento)
admin.site.register(Infracao)
admin.site.register(Seguro)
admin.site.register(Rastreio)
admin.site.register(DespesaViagem)
admin.site.register(FrotaPermissao)
admin.site.register(Manutencao)
admin.site.register(Motorista)
admin.site.register(ItemViagem)
admin.site.register(FrotaBot)
admin.site.register(SolicitacaoViagem)
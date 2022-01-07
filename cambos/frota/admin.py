from django.contrib import admin
from .models import (
    Motorista,
    Veiculo,
    VeiculoAbastecimento,
    Viagem,
    Abastecimento,    
    Infracao,
    Seguro,
    Rastreio,
    DespesaViagem,
    FrotaPermissao,
)

admin.site.register(Motorista)
admin.site.register(Veiculo)
admin.site.register(VeiculoAbastecimento)
admin.site.register(Viagem)
admin.site.register(Abastecimento)
admin.site.register(Infracao)
admin.site.register(Seguro)
admin.site.register(Rastreio)
admin.site.register(DespesaViagem)
admin.site.register(FrotaPermissao)
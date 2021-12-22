from django.contrib import admin
from .models import (
    Motorista,
    Veiculo,
    VeiculoAbastecimento,
    Viagem,
    Abastecimento,
    Corrida,
    Infracao,
    Seguro,
    Rastreio,
    DespesaViagem
)

admin.site.register(Motorista)
admin.site.register(Veiculo)
admin.site.register(VeiculoAbastecimento)
admin.site.register(Viagem)
admin.site.register(Abastecimento)
admin.site.register(Corrida)
admin.site.register(Infracao)
admin.site.register(Seguro)
admin.site.register(Rastreio)
admin.site.register(DespesaViagem)
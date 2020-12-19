from django.contrib import admin
from .models import (   
    Desempenho,
    Material,
    Composicao,
    ValorCompra,
    Consumo,
    Perda,
    Custo,
    Producao
)

admin.site.register(Desempenho)
admin.site.register(Material)
admin.site.register(Composicao)
admin.site.register(ValorCompra)
admin.site.register(Consumo)
admin.site.register(Perda)
admin.site.register(Custo)
admin.site.register(Producao)

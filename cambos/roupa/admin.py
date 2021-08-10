from django.contrib import admin

from .models import (
    Calendario,
    DiasCalendario,
    Processo,
    Etapa,  
    TAG,
    Pedido,
    API,
    PCP,
    PedidoTrack  
)

admin.site.register(Calendario)
admin.site.register(DiasCalendario)
admin.site.register(Processo)
admin.site.register(Etapa)
admin.site.register(TAG)
admin.site.register(Pedido)
admin.site.register(API)
admin.site.register(PCP)
admin.site.register(PedidoTrack)



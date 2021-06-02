from django.contrib import admin

from .models import (
    Calendario,
    DiasCalendario,
    Processo,
    Etapa,    
)

admin.site.register(Calendario)
admin.site.register(DiasCalendario)
admin.site.register(Processo)
admin.site.register(Etapa)


from django.contrib import admin
from .models import (
    User,
    Setor,
    Periodo,
    Bot,
    UserBot,
    OFICINA,
    ACABAMENTO
)

admin.site.register(User)
admin.site.register(Setor)
admin.site.register(Periodo)
admin.site.register(Bot)
admin.site.register(UserBot)
admin.site.register(OFICINA)
admin.site.register(ACABAMENTO)


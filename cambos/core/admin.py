from django.contrib import admin
from .models import (
    User,
    Setor,
    Periodo,
)

admin.site.register(User)
admin.site.register(Setor)
admin.site.register(Periodo)


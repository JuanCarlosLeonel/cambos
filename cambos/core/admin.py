from django.contrib import admin
from .models import (
    User,
    Setor,
    Periodo,
    Bot,
    OFICINA,
    ACABAMENTO
)


class UserAdmin(admin.ModelAdmin):
    list_filter = ['setor','is_active']
    list_display = ['username','email','is_staff','setor']
    search_fields = ['username__startswith']


admin.site.register(User,UserAdmin)
admin.site.register(Setor)
admin.site.register(Periodo)
admin.site.register(Bot)
admin.site.register(OFICINA)
admin.site.register(ACABAMENTO)






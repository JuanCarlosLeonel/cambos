from django.contrib import admin
from .models import (
    User,
    Setor
)

admin.site.register(Setor)
admin.site.register(User)
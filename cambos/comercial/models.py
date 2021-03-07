from django.db import models
from django_currentuser.db.models import CurrentUserField


class Comercial(models.Model):    
    nome    = models.CharField(max_length=18)

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = "Comercial"
from django.db import models
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import AbstractUser

class Setor(models.Model):
    DIVISAO_CHOICES = (
            ('Têxtil', 'Têxtil'),
            ('Confecção', 'Confecção'),             
        )
    nome    = models.CharField(max_length=20)
    divisao = models.CharField(max_length=20, choices=DIVISAO_CHOICES)

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = "Setores"


class User(AbstractUser):
    setor = models.ForeignKey(Setor, null=True, blank=True, on_delete=models.SET_NULL)